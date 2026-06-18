# LINE Scheduled Official Account Sites

這個專案提供本機 Node.js 管理頁，以及可免費部署到 Cloudflare Workers 的韓檢 LINE Bot：

- 金融業國際財金時事：每天早上 `07:30` 推播。
- 韓檢 TOPIK：每天早上 `09:00` 推播 10 個單字，早上 `10:00` 推播 2 個文法。

預設時區是 `Asia/Taipei`。本機可直接預覽內容；接上 LINE Channel Access Token / Channel Secret 後即可部署使用。

## Cloudflare Workers 免費部署

正式韓檢排程設定在 `wrangler.toml`：

```text
0 1 * * *  = 台北時間 09:00 單字
0 2 * * *  = 台北時間 10:00 文法
```

Cloudflare Cron Triggers 使用 UTC。Worker 入口為 `src/worker.js`，需要設定：

```text
LINE_KOREAN_CHANNEL_SECRET
LINE_KOREAN_CHANNEL_ACCESS_TOKEN
LINE_KOREAN_TARGET_IDS
ADMIN_TOKEN
```

## 本機啟動

```bash
cp .env.example .env
npm run dev
```

開啟：

```text
http://localhost:3000
```

## LINE Developers 設定

請為兩個官方帳號各自建立 Messaging API channel，並把 webhook 指到：

```text
https://your-public-domain.example/webhook/finance
https://your-public-domain.example/webhook/korean
```

需要設定的環境變數：

```text
LINE_FINANCE_CHANNEL_ACCESS_TOKEN
LINE_FINANCE_CHANNEL_SECRET
LINE_KOREAN_CHANNEL_ACCESS_TOKEN
LINE_KOREAN_CHANNEL_SECRET
```

使用者加好友或傳訊息後，服務會把 userId 記到 `data/subscribers.json`。若你已經有固定收件者，也可以用逗號分隔填入：

```text
LINE_FINANCE_TARGET_IDS=Uxxxx,Uyyyy
LINE_KOREAN_TARGET_IDS=Uxxxx,Uyyyy
```

## 財金內容來源

財金推播會讀取 `FINANCE_NEWS_RSS_URLS` 的 RSS 標題，組成金融業適用的晨間重點。沒有設定或抓取失敗時，會回退到可預覽的範例內容。

## 手動測試推播

管理頁上每個卡片都有「預覽」和「手動推播」。若 LINE token 尚未設定，手動推播會回傳錯誤但不影響內容預覽。

## 重要檔案

- `src/server.js`：HTTP server、LINE webhook、排程與 API。
- `src/content.js`：財金、韓檢單字、韓檢文法內容產生。
- `src/line.js`：LINE signature 驗證、reply、push。
- `public/index.html`、`public/styles.css`、`public/app.js`：管理網站。
