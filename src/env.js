import { readFileSync } from "node:fs";
import path from "node:path";

export function loadEnv(file = ".env") {
  const envPath = path.resolve(file);
  let content = "";
  try {
    content = readFileSync(envPath, "utf8");
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    return;
  }

  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const equalsIndex = line.indexOf("=");
    if (equalsIndex === -1) continue;
    const key = line.slice(0, equalsIndex).trim();
    const value = line.slice(equalsIndex + 1).trim();
    if (key && process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}
