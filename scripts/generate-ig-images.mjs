import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { koreanGrammarRows, koreanVocabRows } from "../src/content.js";
import { loadEnv } from "../src/env.js";
import { broadcast, configuredTargets, imageMessage, push, textMessage } from "../src/line.js";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
loadEnv(resolve(rootDir, ".env"));

function sleep(ms) {
  return new Promise((resolveSleep) => setTimeout(resolveSleep, ms));
}

function runGit(args, { allowFailure = false } = {}) {
  const result = spawnSync("git", args, {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
  if (!allowFailure && result.status !== 0) process.exit(result.status ?? 1);
  return result;
}

const date = process.env.HANHAN_DATE || new Intl.DateTimeFormat("en-CA", {
  timeZone: "Asia/Taipei",
  year: "numeric",
  month: "2-digit",
  day: "2-digit"
}).format(new Date());

const taipeiTimeParts = new Intl.DateTimeFormat("en-GB", {
  timeZone: "Asia/Taipei",
  hour: "2-digit",
  minute: "2-digit",
  hour12: false
}).formatToParts(new Date());
const taipeiHour = Number(taipeiTimeParts.find((part) => part.type === "hour")?.value ?? "0");
const taipeiMinute = Number(taipeiTimeParts.find((part) => part.type === "minute")?.value ?? "0");
const taipeiMinutes = taipeiHour * 60 + taipeiMinute;
const isScheduledRun = process.env.GITHUB_EVENT_NAME === "schedule";
const shouldRequireMorningWindow = process.env.HANHAN_REQUIRE_TAIPEI_MORNING === "1" && isScheduledRun;
const morningStart = 7 * 60 + 20;
const morningTarget = 7 * 60 + 30;
const morningEnd = 8 * 60 + 30;
const maxWaitMinutes = Number(process.env.HANHAN_MAX_WAIT_MINUTES || "300");

runHanhanWordSeries();

if (shouldRequireMorningWindow && taipeiMinutes < morningStart) {
  const waitMinutes = morningTarget - taipeiMinutes;
  if (waitMinutes > 0 && waitMinutes <= maxWaitMinutes) {
    console.log(
      `HANHAN scheduled run started at ${String(taipeiHour).padStart(2, "0")}:${String(taipeiMinute).padStart(2, "0")} Asia/Taipei; waiting ${waitMinutes} minute(s) to push at 07:30.`
    );
    await sleep(waitMinutes * 60 * 1000);
  } else {
    console.log(
      `Skipped HANHAN LINE push: scheduled run started at ${String(taipeiHour).padStart(2, "0")}:${String(taipeiMinute).padStart(2, "0")} Asia/Taipei, too early to wait safely for 07:30.`
    );
    process.exit(0);
  }
} else if (shouldRequireMorningWindow && taipeiMinutes > morningEnd) {
  console.log(
    `Skipped HANHAN LINE push: scheduled run started at ${String(taipeiHour).padStart(2, "0")}:${String(taipeiMinute).padStart(2, "0")} Asia/Taipei, outside allowed 07:20-08:30 window.`
  );
  process.exit(0);
}

function runHanhanWordSeries() {
  if (process.env.PUSH_HANHAN_WORD_SERIES === "0") return;
  if (!process.env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN) {
    console.warn("Skipped HANHAN word series: missing LINE_HANHAN_CHANNEL_ACCESS_TOKEN.");
    return;
  }

  if (isScheduledRun) {
    runGit(["pull", "--rebase", "origin", "main"], { allowFailure: true });
  }

  const stateRelativePath = "data/hanhan-word-series-state.json";
  const pushResult = spawnSync(
    process.execPath,
    ["scripts/push-hanhan-word-series.mjs"],
    {
      cwd: rootDir,
      env: {
        ...process.env,
        HANHAN_WORD_SERIES_REQUIRE_TAIPEI_MORNING: isScheduledRun ? "1" : "0"
      },
      encoding: "utf8"
    }
  );
  if (pushResult.stdout) process.stdout.write(pushResult.stdout);
  if (pushResult.stderr) process.stderr.write(pushResult.stderr);
  if (pushResult.status !== 0) process.exit(pushResult.status ?? 1);

  if (!isScheduledRun) return;

  const addResult = spawnSync("git", ["add", stateRelativePath], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (addResult.status !== 0) {
    if (addResult.stdout) process.stdout.write(addResult.stdout);
    if (addResult.stderr) process.stderr.write(addResult.stderr);
    process.exit(addResult.status ?? 1);
  }

  const diffResult = spawnSync("git", ["diff", "--cached", "--quiet", "--", stateRelativePath], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (diffResult.status === 0) return;
  if (diffResult.status !== 1) {
    if (diffResult.stdout) process.stdout.write(diffResult.stdout);
    if (diffResult.stderr) process.stderr.write(diffResult.stderr);
    process.exit(diffResult.status ?? 1);
  }

  const commitResult = spawnSync("git", ["commit", "-m", "Update HANHAN word series state", "--", stateRelativePath], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (commitResult.stdout) process.stdout.write(commitResult.stdout);
  if (commitResult.stderr) process.stderr.write(commitResult.stderr);
  if (commitResult.status !== 0) process.exit(commitResult.status ?? 1);

  const gitPushResult = spawnSync("git", ["push", "origin", "main"], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (gitPushResult.stdout) process.stdout.write(gitPushResult.stdout);
  if (gitPushResult.stderr) process.stderr.write(gitPushResult.stderr);
  if (gitPushResult.status !== 0) process.exit(gitPushResult.status ?? 1);
}

const markerPath = resolve(rootDir, "out", "ig", date, `hanhan-pushed-${date}.txt`);
const shouldDedupe = process.env.HANHAN_DEDUPE_GITHUB === "1" && isScheduledRun;

if (shouldDedupe) {
  runGit(["pull", "--rebase", "origin", "main"], { allowFailure: true });
  if (existsSync(markerPath)) {
    console.log(`Skipped HANHAN LINE push: ${date} was already pushed.`);
    process.exit(0);
  }
}

function parsePublishedPost(text) {
  const vocab = new Set();
  const grammar = new Set();
  let section = "";

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("@")) continue;
    if (line === "TOPIK單字") {
      section = "vocab";
      continue;
    }
    if (line === "TOPIK文法") {
      section = "grammar";
      continue;
    }
    if (line.startsWith("意思：")) continue;

    if (section === "vocab") {
      const normalized = line
        .replace(/^\d+\.\s*/, "")
        .replace(/^TOPIK\s+\d+\s*｜\s*/, "");
      const word = normalized.split("｜")[0]?.trim();
      if (word) vocab.add(word);
    }

    if (section === "grammar") {
      const normalized = line.replace(/^\d+\.\s*/, "");
      const match = normalized.match(/^TOPIK\s+\d+\s*｜\s*(.+)$/);
      if (match?.[1]) grammar.add(match[1].trim());
    }
  }

  return { vocab, grammar };
}

function readPublishedHistory(currentDate) {
  const history = { vocab: new Set(), grammar: new Set() };
  const everUsedPath = resolve(rootDir, "data", "hanhan-ever-used.json");
  if (existsSync(everUsedPath)) {
    try {
      const parsed = JSON.parse(readFileSync(everUsedPath, "utf8"));
      for (const word of parsed.vocab || []) history.vocab.add(word);
      for (const pattern of parsed.grammar || []) history.grammar.add(pattern);
    } catch (error) {
      console.warn(`Unable to read HANHAN ever-used history: ${error.message}`);
    }
  }

  const historyPath = resolve(rootDir, "data", "hanhan-published-history.json");
  if (existsSync(historyPath)) {
    try {
      const parsed = JSON.parse(readFileSync(historyPath, "utf8"));
      const byDateEntries = Object.entries(parsed.byDate || {});
      if (byDateEntries.length) {
        for (const [publishedDate, item] of byDateEntries) {
          if (publishedDate >= currentDate) continue;
          for (const word of item.vocab || []) history.vocab.add(word);
          for (const pattern of item.grammar || []) history.grammar.add(pattern);
        }
      } else {
        for (const word of parsed.vocab || []) history.vocab.add(word);
        for (const pattern of parsed.grammar || []) history.grammar.add(pattern);
      }
    } catch (error) {
      console.warn(`Unable to read HANHAN published history: ${error.message}`);
    }
  }

  const igDir = resolve(rootDir, "out", "ig");
  if (!existsSync(igDir)) return history;

  for (const entry of readdirSync(igDir, { withFileTypes: true })) {
    if (!entry.isDirectory() || entry.name >= currentDate) continue;
    const postPath = resolve(igDir, entry.name, `topik-post-${entry.name}.txt`);
    if (!existsSync(postPath)) continue;
    const parsed = parsePublishedPost(readFileSync(postPath, "utf8"));
    for (const word of parsed.vocab) history.vocab.add(word);
    for (const pattern of parsed.grammar) history.grammar.add(pattern);
  }

  return history;
}

function writePublishedHistory(currentDate, textPath) {
  const historyPath = resolve(rootDir, "data", "hanhan-published-history.json");
  const history = existsSync(historyPath)
    ? JSON.parse(readFileSync(historyPath, "utf8"))
    : {};
  const byDate = history.byDate || {};
  const current = parsePublishedPost(readFileSync(textPath, "utf8"));
  byDate[currentDate] = {
    vocab: [...current.vocab],
    grammar: [...current.grammar]
  };

  const vocab = new Set();
  const grammar = new Set();
  for (const item of Object.values(byDate)) {
    for (const word of Array.isArray(item.vocab) ? item.vocab : []) vocab.add(word);
    for (const pattern of Array.isArray(item.grammar) ? item.grammar : []) grammar.add(pattern);
  }

  const updated = {
    generatedAt: new Date().toISOString(),
    byDate: Object.fromEntries(Object.entries(byDate).sort(([a], [b]) => a.localeCompare(b))),
    vocab: [...vocab].sort(),
    grammar: [...grammar].sort()
  };
  writeFileSync(historyPath, `${JSON.stringify(updated, null, 2)}\n`, "utf8");
  return historyPath;
}

const publishedHistory = readPublishedHistory(date);
process.env.HANHAN_EXCLUDE_VOCAB_WORDS = [...publishedHistory.vocab].join("\n");
process.env.HANHAN_EXCLUDE_GRAMMAR_PATTERNS = [...publishedHistory.grammar].join("\n");
console.log(
  `Loaded HANHAN history: ${publishedHistory.vocab.size} vocab word(s), ${publishedHistory.grammar.size} grammar pattern(s) excluded before ${date}.`
);

const payload = {
  date,
  vocab: koreanVocabRows(),
  grammar: koreanGrammarRows()
};

const python = process.env.PYTHON || "python3";
const env = {
  ...process.env,
  PYTHONPATH: [resolve(rootDir, "work/python-packages"), process.env.PYTHONPATH].filter(Boolean).join(":"),
  XDG_DATA_HOME: resolve(rootDir, "work/argos-data"),
  XDG_CONFIG_HOME: resolve(rootDir, "work/argos-config"),
  XDG_CACHE_HOME: resolve(rootDir, "work/argos-cache"),
  ARGOS_PACKAGES_DIR: resolve(rootDir, "work/argos-data/argos-translate/packages")
};

const result = spawnSync(python, [resolve(rootDir, "scripts/render-ig-images.py")], {
  cwd: rootDir,
  env,
  input: JSON.stringify(payload),
  encoding: "utf8"
});

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
if (result.status !== 0) process.exit(result.status ?? 1);

const generatedTextPath = resolve(rootDir, "out", "ig", date, `topik-post-${date}.txt`);
const publishedHistoryPath = writePublishedHistory(date, generatedTextPath);

if (process.env.PUBLISH_HANHAN_IMAGES_GITHUB === "1") {
  const publishPaths = [
    `out/ig/${date}/topik-vocab-${date}.png`,
    `out/ig/${date}/topik-grammar-${date}.png`,
    `out/ig/${date}/topik-post-${date}.txt`,
    publishedHistoryPath.replace(`${rootDir}/`, "")
  ];
  const addResult = spawnSync("git", ["add", "-f", ...publishPaths], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (addResult.status !== 0) {
    if (addResult.stdout) process.stdout.write(addResult.stdout);
    if (addResult.stderr) process.stderr.write(addResult.stderr);
    process.exit(addResult.status ?? 1);
  }

  const diffResult = spawnSync("git", ["diff", "--cached", "--quiet", "--", ...publishPaths], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (diffResult.status === 1) {
    const commitResult = spawnSync("git", ["commit", "-m", `Add ${date} TOPIK assets`, "--", ...publishPaths], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (commitResult.stdout) process.stdout.write(commitResult.stdout);
    if (commitResult.stderr) process.stderr.write(commitResult.stderr);
    if (commitResult.status !== 0) process.exit(commitResult.status ?? 1);
  } else if (diffResult.status === 0) {
    console.log("HANHAN assets already published to GitHub.");
  } else {
    if (diffResult.stdout) process.stdout.write(diffResult.stdout);
    if (diffResult.stderr) process.stderr.write(diffResult.stderr);
    process.exit(diffResult.status ?? 1);
  }

  const pushResult = spawnSync("git", ["push", "origin", "main"], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (pushResult.stdout) process.stdout.write(pushResult.stdout);
  if (pushResult.stderr) process.stderr.write(pushResult.stderr);
  if (pushResult.status !== 0) {
    runGit(["pull", "--rebase", "origin", "main"], { allowFailure: true });
    const retryPushResult = spawnSync("git", ["push", "origin", "main"], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (retryPushResult.stdout) process.stdout.write(retryPushResult.stdout);
    if (retryPushResult.stderr) process.stderr.write(retryPushResult.stderr);
    if (retryPushResult.status === 0) {
      console.log("HANHAN assets pushed to GitHub after remote sync.");
    } else if (shouldDedupe) {
      if (existsSync(markerPath)) {
        console.log(`Skipped HANHAN LINE push: ${date} was already pushed after remote sync.`);
        process.exit(0);
      }
      process.exit(retryPushResult.status ?? 1);
    } else {
      process.exit(retryPushResult.status ?? 1);
    }
  }
}

if (process.env.PUSH_HANHAN_LINE === "1") {
  const textPath = resolve(rootDir, "out", "ig", date, `topik-post-${date}.txt`);
  if (shouldDedupe && existsSync(markerPath)) {
    console.log(`Skipped HANHAN LINE push: ${date} was already pushed.`);
    process.exit(0);
  }

  const text = readFileSync(textPath, "utf8").trim();
  const revisionResult = spawnSync("git", ["rev-parse", "--short", "HEAD"], {
    cwd: rootDir,
    encoding: "utf8"
  });
  const imageVersion = (process.env.HANHAN_IMAGE_VERSION || revisionResult.stdout.trim() || Date.now().toString()).replace(/[^A-Za-z0-9._-]/g, "");
  const configuredImageBaseUrl = process.env.HANHAN_IMAGE_BASE_URL?.replace(/\/$/, "");
  const imageBaseUrl = configuredImageBaseUrl?.startsWith("https://raw.githubusercontent.com/iriswu1991ai/things-of-korean-line-bot/")
    ? `https://cdn.jsdelivr.net/gh/iriswu1991ai/things-of-korean-line-bot@${imageVersion}/out/ig`
    : configuredImageBaseUrl;
  const cacheBuster = `?v=${imageVersion}`;
  const messages = imageBaseUrl ? [
    imageMessage(`${imageBaseUrl}/${date}/topik-vocab-${date}.png${cacheBuster}`),
    imageMessage(`${imageBaseUrl}/${date}/topik-grammar-${date}.png${cacheBuster}`),
    textMessage(text)
  ] : [textMessage(text)];
  const targets = configuredTargets("hanhan");

  if (!process.env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN) {
    console.warn("Skipped HANHAN LINE push: missing LINE_HANHAN_CHANNEL_ACCESS_TOKEN.");
  } else if (targets.length) {
    for (const target of targets) {
      await push("hanhan", target, messages);
    }
    console.log(`Pushed HANHAN LINE text to ${targets.length} target(s).`);
  } else {
    await broadcast("hanhan", messages);
    console.log("Broadcasted HANHAN LINE text.");
  }

  if (shouldDedupe && process.env.PUBLISH_HANHAN_IMAGES_GITHUB === "1") {
    mkdirSync(dirname(markerPath), { recursive: true });
    writeFileSync(markerPath, `${new Date().toISOString()}\n`, "utf8");
    const markerRelativePath = `out/ig/${date}/hanhan-pushed-${date}.txt`;
    const addMarkerResult = spawnSync("git", ["add", "-f", markerRelativePath], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (addMarkerResult.status !== 0) {
      if (addMarkerResult.stdout) process.stdout.write(addMarkerResult.stdout);
      if (addMarkerResult.stderr) process.stderr.write(addMarkerResult.stderr);
      process.exit(addMarkerResult.status ?? 1);
    }

    const commitMarkerResult = spawnSync("git", ["commit", "-m", `Mark ${date} HANHAN push sent`, "--", markerRelativePath], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (commitMarkerResult.stdout) process.stdout.write(commitMarkerResult.stdout);
    if (commitMarkerResult.stderr) process.stderr.write(commitMarkerResult.stderr);
    if (commitMarkerResult.status !== 0) process.exit(commitMarkerResult.status ?? 1);

    const pushMarkerResult = spawnSync("git", ["push", "origin", "main"], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (pushMarkerResult.stdout) process.stdout.write(pushMarkerResult.stdout);
    if (pushMarkerResult.stderr) process.stderr.write(pushMarkerResult.stderr);
    if (pushMarkerResult.status !== 0) {
      runGit(["pull", "--rebase", "origin", "main"], { allowFailure: true });
      if (existsSync(markerPath)) {
        console.log(`Skipped HANHAN LINE marker push: ${date} was already marked after remote sync.`);
        process.exit(0);
      }
      process.exit(pushMarkerResult.status ?? 1);
    }
  }
}
