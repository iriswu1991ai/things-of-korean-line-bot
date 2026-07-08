import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { koreanGrammarRows, koreanVocabRows } from "../src/content.js";
import { loadEnv } from "../src/env.js";
import { broadcast, configuredTargets, imageMessage, push, textMessage } from "../src/line.js";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
loadEnv(resolve(rootDir, ".env"));

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

if (process.env.PUBLISH_HANHAN_IMAGES_GITHUB === "1") {
  const imagePaths = [
    `out/ig/${date}/topik-vocab-${date}.png`,
    `out/ig/${date}/topik-grammar-${date}.png`
  ];
  const addResult = spawnSync("git", ["add", "-f", ...imagePaths], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (addResult.status !== 0) {
    if (addResult.stdout) process.stdout.write(addResult.stdout);
    if (addResult.stderr) process.stderr.write(addResult.stderr);
    process.exit(addResult.status ?? 1);
  }

  const diffResult = spawnSync("git", ["diff", "--cached", "--quiet", "--", ...imagePaths], {
    cwd: rootDir,
    encoding: "utf8"
  });
  if (diffResult.status === 1) {
    const commitResult = spawnSync("git", ["commit", "-m", `Add ${date} TOPIK images`, "--", ...imagePaths], {
      cwd: rootDir,
      encoding: "utf8"
    });
    if (commitResult.stdout) process.stdout.write(commitResult.stdout);
    if (commitResult.stderr) process.stderr.write(commitResult.stderr);
    if (commitResult.status !== 0) process.exit(commitResult.status ?? 1);
  } else if (diffResult.status === 0) {
    console.log("HANHAN images already published to GitHub.");
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
  if (pushResult.status !== 0) process.exit(pushResult.status ?? 1);
}

if (process.env.PUSH_HANHAN_LINE === "1") {
  const textPath = resolve(rootDir, "out", "ig", date, `topik-post-${date}.txt`);
  const text = readFileSync(textPath, "utf8").trim();
  const imageBaseUrl = process.env.HANHAN_IMAGE_BASE_URL?.replace(/\/$/, "");
  const revisionResult = spawnSync("git", ["rev-parse", "--short", "HEAD"], {
    cwd: rootDir,
    encoding: "utf8"
  });
  const imageVersion = (process.env.HANHAN_IMAGE_VERSION || revisionResult.stdout.trim() || Date.now().toString()).replace(/[^A-Za-z0-9._-]/g, "");
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
}
