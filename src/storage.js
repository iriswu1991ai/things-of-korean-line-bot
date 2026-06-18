import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const dataDir = path.resolve("data");
const subscribersPath = path.join(dataDir, "subscribers.json");
const sentLogPath = path.join(dataDir, "sent-log.json");

const defaults = {
  subscribers: { finance: [], korean: [] },
  sentLog: {}
};

async function ensureDataDir() {
  await mkdir(dataDir, { recursive: true });
}

async function readJson(filePath, fallback) {
  await ensureDataDir();
  try {
    return JSON.parse(await readFile(filePath, "utf8"));
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    await writeJson(filePath, fallback);
    return structuredClone(fallback);
  }
}

async function writeJson(filePath, value) {
  await ensureDataDir();
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

export async function getSubscribers(account) {
  const db = await readJson(subscribersPath, defaults.subscribers);
  return db[account] ?? [];
}

export async function addSubscriber(account, userId) {
  if (!userId) return;
  const db = await readJson(subscribersPath, defaults.subscribers);
  const current = new Set(db[account] ?? []);
  current.add(userId);
  db[account] = [...current].sort();
  await writeJson(subscribersPath, db);
}

export async function removeSubscriber(account, userId) {
  if (!userId) return;
  const db = await readJson(subscribersPath, defaults.subscribers);
  db[account] = (db[account] ?? []).filter((id) => id !== userId);
  await writeJson(subscribersPath, db);
}

export async function hasSent(jobKey) {
  const db = await readJson(sentLogPath, defaults.sentLog);
  return Boolean(db[jobKey]);
}

export async function markSent(jobKey) {
  const db = await readJson(sentLogPath, defaults.sentLog);
  db[jobKey] = new Date().toISOString();
  await writeJson(sentLogPath, db);
}
