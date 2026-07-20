import {
  koreanGrammarMessages,
  koreanGrammarRows,
  koreanVocabMessages,
  koreanVocabRows,
  TOPIK_GRAMMAR_COUNT,
  TOPIK_VOCAB_COUNT
} from "./content.js";

const encoder = new TextEncoder();

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" }
  });
}

async function verifySignature(body, signature, secret) {
  if (!signature || !secret) return false;
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const digest = await crypto.subtle.sign("HMAC", key, encoder.encode(body));
  const expected = btoa(String.fromCharCode(...new Uint8Array(digest)));
  return expected === signature;
}

async function lineRequest(path, token, payload) {
  const response = await fetch(`https://api.line.me/v2/bot${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`LINE API ${response.status}: ${await response.text()}`);
  }
}

async function pushToTargets(env, messages) {
  const targets = (env.LINE_KOREAN_TARGET_IDS || "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);

  for (const to of targets) {
    await lineRequest("/message/push", env.LINE_KOREAN_CHANNEL_ACCESS_TOKEN, {
      to,
      messages
    });
  }

  return targets.length;
}

function imageMessage(url) {
  return {
    type: "image",
    originalContentUrl: url,
    previewImageUrl: url
  };
}

function textMessage(text) {
  return { type: "text", text: text.slice(0, 5000) };
}

function todayInTaipei() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Taipei",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date());
}

function daysBetweenTaipeiDates(fromDate, toDate) {
  const from = new Date(`${fromDate}T00:00:00Z`);
  const to = new Date(`${toDate}T00:00:00Z`);
  return Math.floor((to.getTime() - from.getTime()) / 86400000);
}

function taipeiMinutesNow() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Taipei",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return Number(values.hour) * 60 + Number(values.minute);
}

const hanhanWordGroups = [
  {
    key: "맛",
    words: [
      ["맛", "***", "味道"],
      ["맛있다", "***", "好吃"],
      ["맛없다", "***", "不好吃"],
      ["맛보다", "**", "品嘗"],
      ["맛집", "**", "美食店"],
      ["맛보기", "**", "試吃、預覽"],
      ["맛나다", "**", "好吃、有味道"],
      ["맛내다", "**", "調味、做出味道"],
      ["맛깔", "*", "風味、滋味"],
      ["맛소금", "*", "調味鹽"]
    ]
  },
  {
    key: "입",
    words: [
      ["입", "***", "嘴巴"],
      ["입구", "***", "入口"],
      ["입다", "***", "穿"],
      ["입장", "**", "入場、立場"],
      ["입학", "**", "入學"],
      ["입원", "**", "住院"],
      ["입금", "**", "匯款、入帳"],
      ["입맛", "**", "食慾、口味"],
      ["입사", "*", "進公司、入社"],
      ["입국", "*", "入境"]
    ]
  },
  {
    key: "눈",
    words: [
      ["눈", "***", "眼睛、雪"],
      ["눈물", "***", "眼淚"],
      ["눈사람", "***", "雪人"],
      ["눈길", "**", "目光、雪路"],
      ["눈빛", "**", "眼神"],
      ["눈앞", "**", "眼前"],
      ["눈치", "**", "眼色、察言觀色"],
      ["눈병", "**", "眼疾"],
      ["눈썹", "**", "眉毛"],
      ["눈높이", "*", "眼光、標準"]
    ]
  },
  {
    key: "손",
    words: [
      ["손", "***", "手"],
      ["손님", "***", "客人"],
      ["손가락", "***", "手指"],
      ["손목", "**", "手腕"],
      ["손잡이", "**", "把手"],
      ["손질", "**", "整理、修整"],
      ["손해", "**", "損害、虧損"],
      ["손수", "**", "親手"],
      ["손발", "*", "手腳"],
      ["손바닥", "*", "手掌"]
    ]
  },
  {
    key: "물",
    words: [
      ["물", "***", "水"],
      ["물건", "***", "物品、東西"],
      ["물고기", "***", "魚"],
      ["물어보다", "***", "問看看"],
      ["물론", "***", "當然"],
      ["물가", "**", "物價"],
      ["물질", "**", "物質"],
      ["물약", "**", "藥水"],
      ["물속", "*", "水中"],
      ["물음", "*", "問題、提問"]
    ]
  },
  {
    key: "마",
    words: [
      ["마음", "***", "心、心情"],
      ["마시다", "***", "喝"],
      ["마지막", "***", "最後"],
      ["마을", "***", "村子"],
      ["마늘", "**", "大蒜"],
      ["마치다", "**", "結束、完成"],
      ["마중", "**", "迎接"],
      ["마당", "**", "院子"],
      ["마감", "*", "截止、收尾"],
      ["마찰", "*", "摩擦"]
    ]
  },
  {
    key: "바",
    words: [
      ["바다", "***", "海"],
      ["바지", "***", "褲子"],
      ["바람", "***", "風"],
      ["바로", "***", "馬上、正是"],
      ["바쁘다", "***", "忙"],
      ["바꾸다", "***", "更換、改變"],
      ["바닥", "**", "地板、底部"],
      ["바깥", "**", "外面"],
      ["바탕", "*", "基礎、底子"],
      ["바늘", "*", "針"]
    ]
  },
  {
    key: "주",
    words: [
      ["주다", "***", "給"],
      ["주말", "***", "週末"],
      ["주문", "***", "點餐、訂購"],
      ["주소", "***", "地址"],
      ["주로", "**", "主要地"],
      ["주변", "**", "周邊"],
      ["주의", "**", "注意"],
      ["주제", "**", "主題"],
      ["주인", "**", "主人、老闆"],
      ["주차", "**", "停車"]
    ]
  },
  {
    key: "외",
    words: [
      ["외국", "***", "外國"],
      ["외국인", "***", "外國人"],
      ["외우다", "***", "背、記住"],
      ["외출", "**", "外出"],
      ["외롭다", "**", "孤單"],
      ["외모", "**", "外貌"],
      ["외식", "**", "外食、外出用餐"],
      ["외부", "**", "外部"],
      ["외과", "*", "外科"],
      ["외교", "*", "外交"]
    ]
  },
  {
    key: "운",
    words: [
      ["운동", "***", "運動"],
      ["운전", "***", "駕駛"],
      ["운전사", "**", "司機"],
      ["운동장", "**", "運動場"],
      ["운영", "**", "營運、經營"],
      ["운반", "**", "搬運"],
      ["운명", "**", "命運"],
      ["운세", "*", "運勢"],
      ["운임", "*", "運費、車資"],
      ["운하", "*", "運河"]
    ]
  }
];

function hanhanWordSeriesText(date = todayInTaipei()) {
  const startDate = "2026-07-19";
  const startDay = 33;
  const offset = daysBetweenTaipeiDates(startDate, date);
  if (offset < 0) throw new Error(`HANHAN word series date is before start date: ${date}`);
  const group = hanhanWordGroups[offset % hanhanWordGroups.length];
  const day = startDay + offset;

  return [
    `不專業的一起背韓文單字 Day ${day}`,
    "（***韓文1-2급/**韓文3-4급/韓文5-6급）",
    "",
    ...group.words.map(([word, level, meaning]) => `${word} ${level} ${meaning}`)
  ].join("\n");
}

async function pushHanhan(env, messages) {
  const token = env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN;
  if (!token) throw new Error("Missing LINE_HANHAN_CHANNEL_ACCESS_TOKEN");

  const targets = (env.LINE_HANHAN_TARGET_IDS || "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);

  if (targets.length) {
    for (const to of targets) {
      await lineRequest("/message/push", token, { to, messages });
    }
    return { mode: "push", recipients: targets.length };
  }

  await lineRequest("/message/broadcast", token, { messages });
  return { mode: "broadcast", recipients: 0 };
}

async function hanhanDailyMessages(env, date = todayInTaipei()) {
  const imageBaseUrl = (env.HANHAN_IMAGE_BASE_URL || "https://cdn.jsdelivr.net/gh/iriswu1991ai/things-of-korean-line-bot@main/out/ig").replace(/\/$/, "");
  const folderUrl = `${imageBaseUrl}/${date}`;
  const cache = `?v=${date}`;
  const textUrl = `${folderUrl}/topik-post-${date}.txt${cache}`;
  const response = await fetch(textUrl);
  if (!response.ok) throw new Error(`Missing HANHAN text ${date}: ${response.status}`);
  const text = (await response.text()).trim();

  return [
    imageMessage(`${folderUrl}/topik-vocab-${date}.png${cache}`),
    imageMessage(`${folderUrl}/topik-grammar-${date}.png${cache}`),
    textMessage(text)
  ];
}

async function pushHanhanDaily(env, { requireMorningWindow = false } = {}) {
  const minutes = taipeiMinutesNow();
  if (requireMorningWindow && (minutes < 7 * 60 + 20 || minutes > 8 * 60 + 40)) {
    return { ok: true, skipped: true, reason: "outside_taipei_morning_window", minutes };
  }

  const date = todayInTaipei();
  const messages = await hanhanDailyMessages(env, date);
  const result = await pushHanhan(env, messages);
  return { ok: true, date, ...result };
}

async function pushHanhanWordSeries(env, { requireMorningWindow = false } = {}) {
  const minutes = taipeiMinutesNow();
  if (requireMorningWindow && minutes < 8 * 60) {
    return { ok: true, skipped: true, reason: "outside_taipei_word_series_window", minutes };
  }

  const date = todayInTaipei();
  const text = hanhanWordSeriesText(date);
  const result = await pushHanhan(env, [textMessage(text)]);
  return { ok: true, date, kind: "hanhan-word-series", ...result };
}

function parseTranslationArray(value, expectedLength) {
  if (!value) return null;
  const text = typeof value === "string" ? value : value.response;
  if (!text) return null;
  const match = text.match(/\[[\s\S]*\]/);
  if (!match) return null;
  try {
    const parsed = JSON.parse(match[0]);
    return Array.isArray(parsed) && parsed.length === expectedLength
      ? parsed.map(String)
      : null;
  } catch {
    return null;
  }
}

async function translatedVocabMessages(env) {
  const rows = koreanVocabRows();
  if (!env.AI) return koreanVocabMessages(rows);

  try {
    const numbered = rows
      .map((item, index) => `${index + 1}. ${item.exampleKo}`)
      .join("\n");
    const result = await env.AI.run(
      "@cf/meta/llama-3.1-8b-instruct-fp8-fast",
      {
        messages: [
          {
            role: "system",
            content:
              "Translate Korean example sentences into natural Traditional Chinese used in Taiwan. Return only a JSON array of translated strings in the same order. Do not add explanations."
          },
          { role: "user", content: numbered }
        ],
        temperature: 0.1,
        max_tokens: 800
      }
    );
    const translations = parseTranslationArray(result, rows.length);
    if (translations) {
      rows.forEach((item, index) => {
        item.exampleZh = translations[index];
      });
    }
  } catch (error) {
    console.error("Example translation failed:", error);
  }

  return koreanVocabMessages(rows);
}

function parseGrammarDetails(value, rows) {
  const response = value?.response ?? value;
  let parsed = response;
  if (typeof response === "string") {
    try {
      parsed = JSON.parse(response);
    } catch {
      return null;
    }
  }
  const items = parsed?.items;
  if (!Array.isArray(items) || items.length !== rows.length) return null;

  try {
    const detailed = rows.map((row, index) => {
      const detail = items[index];
      if (detail.pattern !== row.pattern) return null;
      const examples = Array.isArray(detail.examples)
        ? detail.examples
            .slice(0, 2)
            .map((example) => ({
              ko: String(example.ko || "").trim(),
              zh: String(example.zh || "").trim(),
              applied: String(example.applied || "").trim()
            }))
            .filter(
              (example) =>
                example.ko &&
                example.zh &&
                example.applied.length >= 2 &&
                /[가-힣]/.test(example.applied) &&
                example.ko.includes(example.applied)
            )
        : [];
      if (examples.length !== 2) return null;
      return {
        ...row,
        attachment: String(detail.attachment || row.attachment),
        meaning: String(detail.meaning || row.meaning),
        examples: examples.map((example) => [example.ko, example.zh])
      };
    });
    return detailed.every(Boolean) ? detailed : null;
  } catch {
    return null;
  }
}

function hasPlaceholderExample(rows) {
  const invalidPhrases = [
    "문법을 공부합니다",
    "문법을 사용해 보세요",
    "문법을 연습합니다",
    "今天學習這個韓語文法",
    "請嘗試依照語境使用這個文法"
  ];
  return rows.some((row) =>
    row.examples.some(([ko, zh]) =>
      invalidPhrases.some((phrase) => ko.includes(phrase) || zh.includes(phrase))
    )
  );
}

async function generatedGrammarMessages(env) {
  const rows = koreanGrammarRows();
  if (rows.every((row) => row.examples.length === 2)) {
    return koreanGrammarMessages(rows);
  }
  if (!env.AI) return koreanGrammarMessages(rows);

  const grammarList = rows
    .map((item, index) => `${index + 1}. TOPIK ${item.level}: ${item.pattern}`)
    .join("\n");
  const responseFormat = {
    type: "json_schema",
    json_schema: {
      type: "object",
      properties: {
        items: {
          type: "array",
          minItems: 2,
          maxItems: 2,
          items: {
            type: "object",
            properties: {
              pattern: { type: "string" },
              attachment: { type: "string" },
              meaning: { type: "string" },
              examples: {
                type: "array",
                minItems: 2,
                maxItems: 2,
                items: {
                  type: "object",
                  properties: {
                    ko: { type: "string" },
                    zh: { type: "string" },
                    applied: { type: "string" }
                  },
                  required: ["ko", "zh", "applied"],
                  additionalProperties: false
                }
              }
            },
            required: ["pattern", "attachment", "meaning", "examples"],
            additionalProperties: false
          }
        }
      },
      required: ["items"],
      additionalProperties: false
    }
  };

  for (let attempt = 1; attempt <= 2; attempt += 1) {
    try {
      const result = await env.AI.run(
        "@cf/meta/llama-3.1-8b-instruct-fast",
        {
        messages: [
          {
            role: "system",
            content:
              "You are a meticulous Korean language teacher. For each fixed grammar pattern, provide accurate attachment rules, a concise Traditional Chinese explanation used in Taiwan, and exactly two natural Korean example sentences that genuinely use that grammar. For each example, applied must be the exact conjugated Korean substring appearing verbatim inside ko that realizes the requested grammar. Never write meta sentences about studying, practicing, or using grammar. Preserve each pattern exactly and keep the input order."
          },
          { role: "user", content: grammarList }
        ],
        temperature: 0.1,
          max_tokens: 1400,
          response_format: responseFormat
        }
      );
      const detailed = parseGrammarDetails(result, rows);
      if (detailed && !hasPlaceholderExample(detailed)) {
        return koreanGrammarMessages(detailed);
      }
      console.error(`Grammar validation failed on attempt ${attempt}`);
    } catch (error) {
      console.error(`Grammar generation attempt ${attempt} failed:`, error);
    }
  }

  throw new Error("Grammar content generation failed validation; push cancelled");
}

async function handleWebhook(request, env) {
  const body = await request.text();
  const valid = await verifySignature(
    body,
    request.headers.get("x-line-signature"),
    env.LINE_KOREAN_CHANNEL_SECRET
  );
  if (!valid) return json({ error: "Invalid LINE signature" }, 401);

  return json({ ok: true });
}

async function handleAdminPush(request, env) {
  return json({ ok: false, linePushStatus: "paused", error: "LINE push is paused" }, 423);

  if (!env.ADMIN_TOKEN || request.headers.get("x-admin-token") !== env.ADMIN_TOKEN) {
    return json({ error: "Admin token required" }, 401);
  }

  const { kind } = await request.json();
  const messages =
    kind === "korean-vocab" ? await translatedVocabMessages(env) :
    kind === "korean-grammar" ? await generatedGrammarMessages(env) :
    null;
  if (!messages) return json({ error: "Unknown push kind" }, 400);

  const recipients = await pushToTargets(env, messages);
  return json({ ok: true, recipients });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "POST" && url.pathname === "/webhook/korean") {
      return handleWebhook(request, env);
    }

    if (request.method === "POST" && url.pathname === "/api/push") {
      return handleAdminPush(request, env);
    }

    if (request.method === "POST" && url.pathname === "/api/hanhan-daily") {
      if (!env.ADMIN_PUSH_SECRET || request.headers.get("Authorization") !== `Bearer ${env.ADMIN_PUSH_SECRET}`) {
        return json({ error: "Unauthorized" }, 401);
      }
      return json(await pushHanhanDaily(env));
    }

    if (url.pathname === "/healthz" || url.pathname === "/") {
      return json({
        ok: true,
        service: "Things of Korean LINE Bot",
        vocabularyCount: TOPIK_VOCAB_COUNT,
        grammarCount: TOPIK_GRAMMAR_COUNT,
        grammarValidation: "strict",
        grammarContentMode: "fixed-examples-first",
        levelRotation: "mixed-daily",
        linePushStatus: "hanhan-worker-enabled",
        manualPushStatus: "hanhan-daily-enabled",
        hanhanTokenConfigured: Boolean(env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN),
        hanhanImageBaseConfigured: Boolean(env.HANHAN_IMAGE_BASE_URL),
        schedules: ["30 23 * * *"]
      });
    }

    return json({ error: "Not found" }, 404);
  },

  async scheduled(controller, env) {
    const result = controller.cron === "0 0 * * *"
      ? await pushHanhanWordSeries(env, { requireMorningWindow: true })
      : await pushHanhanDaily(env, { requireMorningWindow: true });
    console.log(`HANHAN scheduled ${controller.cron}: ${JSON.stringify(result)}`);
  }
};
