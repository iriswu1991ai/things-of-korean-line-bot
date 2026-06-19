import http from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { loadEnv } from "./env.js";
import { addSubscriber, getSubscribers, hasSent, markSent, removeSubscriber } from "./storage.js";
import { configuredTargets, push, verifySignature } from "./line.js";
import { financeMessages, koreanGrammarMessages, koreanVocabMessages, preview } from "./content.js";
import { isScheduledTime, nowParts } from "./time.js";

loadEnv();

const port = Number(process.env.PORT || 3000);
const publicDir = path.resolve("public");
const timeZone = process.env.TIMEZONE || "Asia/Taipei";

const jobs = [
  { key: "finance-0730", account: "finance", hour: "07", minute: "30", build: financeMessages },
  { key: "korean-vocab-0900", account: "korean", hour: "09", minute: "00", build: koreanVocabMessages },
  { key: "korean-grammar-1000", account: "korean", hour: "10", minute: "00", build: koreanGrammarMessages }
];

function sendJson(res, status, payload) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
}

function isAuthorized(req) {
  const token = process.env.ADMIN_TOKEN;
  if (!token) return true;
  return req.headers["x-admin-token"] === token;
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function serveStatic(req, res) {
  const requested = req.url === "/" ? "/index.html" : new URL(req.url, "http://localhost").pathname;
  const safePath = path.normalize(requested).replace(/^(\.\.[/\\])+/, "");
  const filePath = path.join(publicDir, safePath);
  const ext = path.extname(filePath);
  const types = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8"
  };
  try {
    const content = await readFile(filePath);
    res.writeHead(200, { "Content-Type": types[ext] || "application/octet-stream" });
    res.end(content);
  } catch {
    sendJson(res, 404, { error: "Not found" });
  }
}

async function recipientsFor(account) {
  const configured = configuredTargets(account);
  if (configured.length) return configured;
  return getSubscribers(account);
}

async function pushToAccount(account, messages) {
  const recipients = await recipientsFor(account);
  const results = [];
  for (const userId of recipients) {
    try {
      await push(account, userId, messages);
      results.push({ userId, ok: true });
    } catch (error) {
      results.push({ userId, ok: false, error: error.message });
    }
  }
  return { recipients: recipients.length, results };
}

async function handleWebhook(account, req, res) {
  const body = await readBody(req);
  const signature = req.headers["x-line-signature"];
  if (!verifySignature(account, body, signature)) {
    sendJson(res, 401, { error: "Invalid LINE signature" });
    return;
  }

  const payload = JSON.parse(body);
  for (const event of payload.events ?? []) {
    const userId = event.source?.userId;
    if (event.type === "follow" || event.type === "message") {
      await addSubscriber(account, userId);
    }
    if (event.type === "unfollow") {
      await removeSubscriber(account, userId);
    }
  }

  sendJson(res, 200, { ok: true });
}

async function handleApi(req, res) {
  const url = new URL(req.url, "http://localhost");

  if (req.method === "GET" && url.pathname === "/api/status") {
    const [finance, korean] = await Promise.all([getSubscribers("finance"), getSubscribers("korean")]);
    sendJson(res, 200, {
      timeZone,
      now: nowParts(timeZone),
      subscribers: { finance: finance.length, korean: korean.length },
      schedules: jobs.map(({ key, account, hour, minute }) => ({ key, account, time: `${hour}:${minute}` }))
    });
    return;
  }

  if (req.method === "GET" && url.pathname === "/api/preview") {
    const kind = url.searchParams.get("kind");
    sendJson(res, 200, { kind, messages: await preview(kind) });
    return;
  }

  if (req.method === "POST" && url.pathname === "/api/push") {
    if (!isAuthorized(req)) {
      sendJson(res, 401, { error: "Admin token required" });
      return;
    }
    const body = JSON.parse((await readBody(req)) || "{}");
    const messages = await preview(body.kind);
    const account = body.kind === "finance" ? "finance" : "korean";
    sendJson(res, 200, await pushToAccount(account, messages));
    return;
  }

  sendJson(res, 404, { error: "Unknown API route" });
}

async function handleRequest(req, res) {
  try {
    const url = new URL(req.url, "http://localhost");
    if (req.method === "POST" && url.pathname === "/webhook/finance") {
      await handleWebhook("finance", req, res);
      return;
    }
    if (req.method === "POST" && url.pathname === "/webhook/korean") {
      await handleWebhook("korean", req, res);
      return;
    }
    if (req.method === "GET" && url.pathname === "/healthz") {
      sendJson(res, 200, { ok: true, now: nowParts(timeZone) });
      return;
    }
    if (url.pathname.startsWith("/api/")) {
      await handleApi(req, res);
      return;
    }
    await serveStatic(req, res);
  } catch (error) {
    sendJson(res, 500, { error: error.message });
  }
}

async function runDueJobs() {
  for (const job of jobs) {
    if (!isScheduledTime(job.hour, job.minute, timeZone)) continue;
    const key = `${nowParts(timeZone).date}:${job.key}`;
    if (await hasSent(key)) continue;
    const messages = await job.build();
    await pushToAccount(job.account, messages);
    await markSent(key);
  }
}

http.createServer(handleRequest).listen(port, () => {
  console.log(`LINE scheduled sites running at http://localhost:${port}`);
  console.log(`Timezone: ${timeZone}`);
});

setInterval(() => {
  runDueJobs().catch((error) => console.error("Scheduled job failed:", error));
}, 30_000);
