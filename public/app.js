const statusEl = document.querySelector("#status");
const previewEl = document.querySelector("#preview");
const resultEl = document.querySelector("#result");

async function api(path, options) {
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Request failed");
  return payload;
}

async function refreshStatus() {
  const status = await api("/api/status");
  statusEl.textContent = `${status.now.date} ${status.now.hour}:${status.now.minute}｜財金 ${status.subscribers.finance}｜韓檢 ${status.subscribers.korean}`;
}

async function showPreview(kind) {
  resultEl.textContent = "預覽已更新";
  const payload = await api(`/api/preview?kind=${encodeURIComponent(kind)}`);
  previewEl.textContent = payload.messages.map(renderMessagePreview).join("\n\n---\n\n");
}

function renderMessagePreview(message) {
  if (message.type === "text") return message.text;
  if (message.type === "flex") {
    const bubbles = message.contents?.contents ?? [];
    const cards = bubbles.map((bubble, index) => {
      const title = findTexts(bubble.header).slice(-1)[0] || `卡片 ${index + 1}`;
      const details = findTexts(bubble.body).join("\n");
      return `${index + 1}. ${title}\n${details}`;
    });
    return [`Flex Message｜${message.altText}`, "", cards.join("\n\n")].join("\n");
  }
  return JSON.stringify(message, null, 2);
}

function findTexts(node) {
  if (!node) return [];
  if (Array.isArray(node)) return node.flatMap(findTexts);
  if (typeof node !== "object") return [];
  const current = node.type === "text" && node.text ? [node.text] : [];
  return [...current, ...findTexts(node.contents)];
}

async function pushNow(kind) {
  resultEl.textContent = "推播中";
  const options = {
    method: "POST",
    headers: adminHeaders(),
    body: JSON.stringify({ kind })
  };
  let payload;
  try {
    payload = await api("/api/push", options);
  } catch (error) {
    if (error.message !== "Admin token required") throw error;
    const token = window.prompt("請輸入管理密碼");
    if (!token) throw error;
    sessionStorage.setItem("adminToken", token);
    options.headers = adminHeaders();
    payload = await api("/api/push", options);
  }
  resultEl.textContent = `已嘗試推播 ${payload.recipients} 位收件者`;
}

function adminHeaders() {
  const headers = { "Content-Type": "application/json" };
  const token = sessionStorage.getItem("adminToken");
  if (token) headers["X-Admin-Token"] = token;
  return headers;
}

document.addEventListener("click", async (event) => {
  const previewKind = event.target.dataset.preview;
  const pushKind = event.target.dataset.push;
  try {
    if (previewKind) await showPreview(previewKind);
    if (pushKind) await pushNow(pushKind);
  } catch (error) {
    resultEl.textContent = error.message;
  }
});

refreshStatus().catch((error) => {
  statusEl.textContent = error.message;
});
setInterval(refreshStatus, 30_000);
