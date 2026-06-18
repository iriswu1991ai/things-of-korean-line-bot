# Things of Korean 免費正式版

平台：Cloudflare Workers Free

## 排程

- `0 1 * * *`：台北時間每天 09:00 推播韓檢單字
- `0 2 * * *`：台北時間每天 10:00 推播韓檢文法

Cloudflare Cron Triggers 使用 UTC。

## Cloudflare Secrets

```text
LINE_KOREAN_CHANNEL_SECRET
LINE_KOREAN_CHANNEL_ACCESS_TOKEN
LINE_KOREAN_TARGET_IDS
ADMIN_TOKEN
```

## Webhook

部署後網址會類似：

```text
https://things-of-korean-line-bot.<帳號>.workers.dev
```

LINE Developers Webhook URL：

```text
https://things-of-korean-line-bot.<帳號>.workers.dev/webhook/korean
```
