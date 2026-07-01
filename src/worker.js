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

    if (url.pathname === "/healthz" || url.pathname === "/") {
      return json({
        ok: true,
        service: "Things of Korean LINE Bot",
        vocabularyCount: TOPIK_VOCAB_COUNT,
        grammarCount: TOPIK_GRAMMAR_COUNT,
        grammarValidation: "strict",
        grammarContentMode: "fixed-examples-first",
        levelRotation: "mixed-daily",
        linePushStatus: "paused",
        manualPushStatus: "paused",
        schedules: []
      });
    }

    return json({ error: "Not found" }, 404);
  },

  async scheduled(controller) {
    console.log(`LINE scheduled push is paused; ignored cron ${controller.cron}`);
  }
};
