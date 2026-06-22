import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { loadEnv } from "../src/env.js";

loadEnv();

const apiKey = process.env.KRDICT_API_KEY;
if (!apiKey) throw new Error("KRDICT_API_KEY is required in .env");

const workDir = path.resolve("work/krdict");
const indexPath = path.join(workDir, "index.json");
const indexStatePath = path.join(workDir, "index-state.json");
const coreIndexPath = path.join(workDir, "core-index.json");
const entriesPath = path.join(workDir, "entries.json");
const statePath = path.join(workDir, "state.json");
const maxConcurrency = Number(process.env.KRDICT_CONCURRENCY || 8);
const indexVersion = 2;
const selectionVersion = 3;

await mkdir(workDir, { recursive: true });

function decodeXml(value = "") {
  return value
    .replace(/^<!\[CDATA\[|\]\]>$/g, "")
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'")
    .trim();
}

function tag(block, name) {
  const match = block.match(new RegExp(`<${name}>([\\s\\S]*?)</${name}>`));
  return decodeXml(match?.[1]);
}

async function readJson(filePath, fallback) {
  try {
    return JSON.parse(await readFile(filePath, "utf8"));
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    return fallback;
  }
}

async function saveJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

async function api(pathname, params) {
  const url = new URL(`https://krdict.korean.go.kr/api/${pathname}`);
  url.searchParams.set("key", apiKey);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, String(value));
  }

  for (let attempt = 1; attempt <= 4; attempt += 1) {
    const response = await fetch(url);
    if (response.ok) return response.text();
    if (attempt === 4) {
      throw new Error(`Krdict API ${response.status}: ${await response.text()}`);
    }
    await new Promise((resolve) => setTimeout(resolve, attempt * 500));
  }
}

function parseSearch(xml) {
  return [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)]
    .map((match) => {
      const block = match[1];
      return {
        targetCode: tag(block, "target_code"),
        word: tag(block, "word"),
        grade: tag(block, "word_grade"),
        pos: tag(block, "pos")
      };
    })
    .filter((item) => item.targetCode && item.grade);
}

function parseTotal(xml) {
  return Number(tag(xml, "total") || 0);
}

async function searchSyllable(syllable) {
  const params = {
    q: syllable,
    advanced: "y",
    method: "start",
    translated: "y",
    trans_lang: 11,
    num: 100
  };
  const firstXml = await api("search", params);
  const total = parseTotal(firstXml);
  const items = parseSearch(firstXml);

  for (let start = 101; start <= Math.min(total, 1000); start += 100) {
    const xml = await api("search", { ...params, start });
    items.push(...parseSearch(xml));
  }

  return items;
}

function parseView(xml, fallback) {
  const word = tag(xml, "word") || fallback.word;
  const grade = tag(xml, "word_grade") || fallback.grade;
  const pos = tag(xml, "pos") || fallback.pos;
  const firstSense = xml.match(/<sense_info>([\s\S]*?)<\/sense_info>/)?.[1] || xml;
  const translation = tag(firstSense, "trans_word");
  const definitionZh = tag(firstSense, "trans_dfn");
  const examples = [...firstSense.matchAll(/<example>([\s\S]*?)<\/example>/g)]
    .map((match) => decodeXml(match[1]))
    .filter((example) => example.length >= 12 && /[.!?。]$/.test(example));

  return {
    id: fallback.targetCode,
    word,
    topikLevel: fallback.topikLevel,
    grade,
    pos,
    translation,
    definitionZh,
    exampleKo: examples[0] || "",
    exampleZh: "",
    source: "한국어기초사전",
    sourceUrl: `https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=${fallback.targetCode}`
  };
}

function selectCoreVocabulary(index, frequencies) {
  const gradeRank = { 초급: 0, 중급: 1, 고급: 2 };
  const excludedPos = new Set(["", "품사 없음", "접사", "조사"]);
  const uniqueWords = new Map();

  for (const item of index) {
    if (
      excludedPos.has(item.pos) ||
      !/[가-힣]/.test(item.word) ||
      item.word.includes("-") ||
      (item.grade === "고급" && item.word.length === 1)
    ) {
      continue;
    }
    const current = uniqueWords.get(item.word);
    if (!current || gradeRank[item.grade] < gradeRank[current.grade]) {
      uniqueWords.set(item.word, item);
    }
  }

  const byGrade = { 초급: [], 중급: [], 고급: [] };
  for (const item of uniqueWords.values()) byGrade[item.grade].push(item);
  for (const items of Object.values(byGrade)) {
    items.sort(
      (a, b) =>
        (frequencies[b.word] || 0) - (frequencies[a.word] || 0) ||
        a.word.length - b.word.length ||
        a.word.localeCompare(b.word, "ko") ||
        Number(a.targetCode) - Number(b.targetCode)
    );
  }

  const selected = [
    ...byGrade["초급"],
    ...byGrade["중급"].slice(0, 2448),
    ...byGrade["고급"].slice(0, 2000)
  ];
  const groups = {
    초급: selected.filter((item) => item.grade === "초급"),
    중급: selected.filter((item) => item.grade === "중급"),
    고급: selected.filter((item) => item.grade === "고급")
  };

  return Object.entries(groups).flatMap(([grade, items]) => {
    const baseLevel = grade === "초급" ? 1 : grade === "중급" ? 3 : 5;
    const splitAt = Math.ceil(items.length / 2);
    return items.map((item, index) => ({
      ...item,
      topikLevel: baseLevel + (index >= splitAt ? 1 : 0)
    }));
  });
}

async function mapLimit(values, limit, worker) {
  let cursor = 0;
  const results = [];
  async function run() {
    while (cursor < values.length) {
      const index = cursor++;
      results[index] = await worker(values[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, values.length) }, run));
  return results;
}

async function buildIndex() {
  const existing = await readJson(indexPath, []);
  if (existing.length) return existing;

  const allSyllables = Array.from(
    { length: 0xD7A3 - 0xAC00 + 1 },
    (_, index) => String.fromCharCode(0xAC00 + index)
  );
  const maxSyllables = Number(process.env.KRDICT_MAX_SYLLABLES || allSyllables.length);
  const savedCheckpoint = await readJson(indexStatePath, {
    version: indexVersion,
    completed: [],
    items: []
  });
  const checkpoint =
    savedCheckpoint.version === indexVersion
      ? savedCheckpoint
      : { version: indexVersion, completed: [], items: [] };
  const completed = new Set(checkpoint.completed);
  const found = new Map(checkpoint.items.map((item) => [item.targetCode, item]));
  const syllables = allSyllables
    .filter((syllable) => !completed.has(syllable))
    .slice(0, maxSyllables);
  let processed = 0;

  await mapLimit(syllables, maxConcurrency, async (syllable) => {
    for (const item of await searchSyllable(syllable)) {
      found.set(item.targetCode, item);
    }
    completed.add(syllable);
    processed += 1;
    if (processed % 250 === 0) {
      await saveJson(indexStatePath, {
        version: indexVersion,
        completed: [...completed],
        items: [...found.values()]
      });
      process.stdout.write(`Indexed ${processed}/${syllables.length}; found ${found.size}\n`);
    }
  });

  await saveJson(indexStatePath, {
    version: indexVersion,
    completed: [...completed],
    items: [...found.values()]
  });

  if (completed.size < allSyllables.length) {
    console.log(`Index checkpoint saved: ${completed.size}/${allSyllables.length} syllables`);
    return [];
  }

  const index = [...found.values()].sort((a, b) =>
    a.grade.localeCompare(b.grade, "ko") || a.word.localeCompare(b.word, "ko")
  );
  await saveJson(indexPath, index);
  return index;
}

async function buildEntries(index) {
  const selectedIds = new Set(index.map((item) => item.targetCode));
  const entries = (await readJson(entriesPath, [])).filter((entry) =>
    selectedIds.has(entry.id)
  );
  const savedState = await readJson(statePath, {
    selectionVersion,
    completed: []
  });
  const stateMatches = savedState.selectionVersion === selectionVersion;
  const state = stateMatches
    ? savedState
    : { selectionVersion, completed: entries.map((entry) => entry.id) };
  const completed = new Set(state.completed);
  const byId = new Map(entries.map((entry) => [entry.id, entry]));
  for (const item of index) {
    const entry = byId.get(item.targetCode);
    if (entry) {
      entry.topikLevel = item.topikLevel;
      entry.grade = item.grade;
      entry.pos = item.pos;
    }
  }
  const pending = index.filter((item) => !completed.has(item.targetCode));
  let processed = 0;

  await mapLimit(pending, maxConcurrency, async (item) => {
    const xml = await api("view", {
      method: "target_code",
      q: item.targetCode,
      translated: "y",
      trans_lang: 11
    });
    byId.set(item.targetCode, parseView(xml, item));
    completed.add(item.targetCode);
    processed += 1;

    if (processed % 50 === 0 || processed === pending.length) {
      await saveJson(entriesPath, [...byId.values()]);
      await saveJson(statePath, {
        selectionVersion,
        completed: [...completed]
      });
      process.stdout.write(`Fetched ${processed}/${pending.length} entries\n`);
    }
  });

  const orderedEntries = index
    .map((item) => byId.get(item.targetCode))
    .filter(Boolean);
  await saveJson(entriesPath, orderedEntries);
  await saveJson(statePath, {
    selectionVersion,
    completed: [...completed]
  });
  return orderedEntries;
}

const index = await buildIndex();
console.log(`Learning vocabulary index: ${index.length}`);
const frequencies = await readJson(path.join(workDir, "frequencies.json"), {});
if (!Object.keys(frequencies).length) {
  throw new Error("Run scripts/prepare-krdict.py before selecting core vocabulary");
}
const coreIndex = selectCoreVocabulary(index, frequencies);
await saveJson(coreIndexPath, coreIndex);
console.log(`Selected core vocabulary: ${coreIndex.length}`);
const entries = await buildEntries(coreIndex);
console.log(`Dictionary entries: ${entries.length}`);
