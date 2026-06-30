import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { koreanGrammarRows, koreanVocabRows } from "../src/content.js";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const date = new Intl.DateTimeFormat("en-CA", {
  timeZone: "Asia/Taipei",
  year: "numeric",
  month: "2-digit",
  day: "2-digit"
}).format(new Date());

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
