import { koreanGrammarMessages, koreanVocabMessages } from "./content.js";

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
  if (!env.ADMIN_TOKEN || request.headers.get("x-admin-token") !== env.ADMIN_TOKEN) {
    return json({ error: "Admin token required" }, 401);
  }

  const { kind } = await request.json();
  const messages =
    kind === "korean-vocab" ? koreanVocabMessages() :
    kind === "korean-grammar" ? koreanGrammarMessages() :
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
        schedules: ["09:00 Asia/Taipei vocabulary", "10:00 Asia/Taipei grammar"]
      });
    }

    return json({ error: "Not found" }, 404);
  },

  async scheduled(controller, env, ctx) {
    const messages =
      controller.cron === "0 1 * * *"
        ? koreanVocabMessages()
        : controller.cron === "0 2 * * *"
          ? koreanGrammarMessages()
          : null;

    if (messages) {
      ctx.waitUntil(pushToTargets(env, messages));
    }
  }
};
