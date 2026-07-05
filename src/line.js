import crypto from "node:crypto";

const accounts = {
  finance: {
    token: () => process.env.LINE_FINANCE_CHANNEL_ACCESS_TOKEN,
    secret: () => process.env.LINE_FINANCE_CHANNEL_SECRET,
    targetIds: () => parseIds(process.env.LINE_FINANCE_TARGET_IDS)
  },
  korean: {
    token: () => process.env.LINE_KOREAN_CHANNEL_ACCESS_TOKEN,
    secret: () => process.env.LINE_KOREAN_CHANNEL_SECRET,
    targetIds: () => parseIds(process.env.LINE_KOREAN_TARGET_IDS)
  },
  hanhan: {
    token: () => process.env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN,
    secret: () => process.env.LINE_HANHAN_CHANNEL_SECRET,
    targetIds: () => parseIds(process.env.LINE_HANHAN_TARGET_IDS)
  }
};

function parseIds(value = "") {
  return value
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
}

export function verifySignature(account, body, signature) {
  const secret = accounts[account]?.secret();
  if (!secret || !signature) return false;
  const digest = crypto.createHmac("sha256", secret).update(body).digest("base64");
  const expected = Buffer.from(digest);
  const actual = Buffer.from(signature);
  if (expected.length !== actual.length) return false;
  return crypto.timingSafeEqual(expected, actual);
}

async function lineRequest(account, path, payload) {
  const token = accounts[account]?.token();
  if (!token) {
    throw new Error(`Missing LINE access token for ${account}`);
  }

  const response = await fetch(`https://api.line.me/v2/bot${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`LINE API ${response.status}: ${detail}`);
  }
}

export async function reply(account, replyToken, messages) {
  if (!replyToken) return;
  await lineRequest(account, "/message/reply", { replyToken, messages });
}

export async function push(account, to, messages) {
  await lineRequest(account, "/message/push", { to, messages });
}

export async function broadcast(account, messages) {
  await lineRequest(account, "/message/broadcast", { messages });
}

export function configuredTargets(account) {
  return accounts[account]?.targetIds() ?? [];
}

export function textMessage(text) {
  return { type: "text", text: text.slice(0, 5000) };
}

export function imageMessage(url) {
  return {
    type: "image",
    originalContentUrl: url,
    previewImageUrl: url
  };
}
