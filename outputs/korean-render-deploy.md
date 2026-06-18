# Things of Korean 測試正式版部署清單

## 建議平台

先用 Render Web Service。注意：免費 Web Service 會休眠，不適合準時排程推播；測試每日 09:00 / 10:00 準時推播請選 always-on 的付費 instance。

## Render 設定

- Service type: Web Service
- Runtime: Node
- Build command: `npm install`
- Start command: `npm start`
- Health check path: `/healthz`
- Timezone env: `Asia/Taipei`

## 必填環境變數

```env
TIMEZONE=Asia/Taipei
LINE_KOREAN_CHANNEL_SECRET=貼上 LINE Developers 的 Channel secret
LINE_KOREAN_CHANNEL_ACCESS_TOKEN=貼上 LINE Developers 的 Channel access token
LINE_KOREAN_TARGET_IDS=貼上目前測試者的 LINE userId
ADMIN_TOKEN=自己設定一組管理密碼
```

## 部署後

部署完成後 Render 會給一個網址，格式通常像：

```text
https://things-of-korean-line-bot.onrender.com
```

到 LINE Developers Console 的 Messaging API 分頁，把 Webhook URL 改成：

```text
https://你的-render-網址/webhook/korean
```

然後按 Verify，成功後打開 Use webhook。
