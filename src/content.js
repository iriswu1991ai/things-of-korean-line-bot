import topikVocab from "../data/topik-vocab.json" with { type: "json" };

function textMessage(text) {
  return { type: "text", text: text.slice(0, 5000) };
}

const financeFallback = [
  "美國利率預期與美元走勢仍是今日市場定價主軸。",
  "亞洲股匯市需留意科技股財報、資金輪動與央行官員談話。",
  "原油與黃金價格可作為通膨預期、避險需求與實質利率變化的觀察指標。",
  "金融業今日可聚焦授信曝險、外幣部位與客戶再平衡需求。"
];

const grammarBank = [
  {
    pattern: "-(으)ㄴ/는 반면에",
    meaning: "表示對比，相當於「相反地、另一方面」。",
    examples: [
      ["이 제품은 품질이 좋은 반면에 가격이 비쌉니다.", "這個產品品質好，但價格昂貴。"],
      ["도시는 편리한 반면에 생활비가 많이 듭니다.", "都市很便利，但生活費很高。"]
    ]
  },
  {
    pattern: "-기 마련이다",
    meaning: "表示某事通常會自然發生，相當於「必然、總是會」。",
    examples: [
      ["노력하면 실력이 늘기 마련입니다.", "努力的話，實力自然會進步。"],
      ["사람은 누구나 실수하기 마련입니다.", "人難免都會犯錯。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 뿐만 아니라",
    meaning: "表示不只前項，後項也成立，相當於「不僅...而且...」。",
    examples: [
      ["그는 한국어를 잘할 뿐만 아니라 일본어도 잘합니다.", "他不只韓文好，日文也好。"],
      ["이 방법은 간단할 뿐만 아니라 효과도 큽니다.", "這個方法不僅簡單，而且效果也大。"]
    ]
  },
  {
    pattern: "-도록",
    meaning: "表示目的、程度或使役方向，相當於「為了、直到」。",
    examples: [
      ["늦지 않도록 일찍 출발하세요.", "請早點出發以免遲到。"],
      ["모두가 이해하도록 천천히 설명했습니다.", "為了讓大家理解，慢慢地說明了。"]
    ]
  },
  {
    pattern: "-는 바람에",
    meaning: "表示因意外原因造成負面結果，相當於「因為...結果...」。",
    examples: [
      ["버스를 놓치는 바람에 약속에 늦었습니다.", "因為錯過公車，結果約會遲到了。"],
      ["비가 많이 오는 바람에 경기가 취소되었습니다.", "因為下大雨，比賽被取消了。"]
    ]
  },
  {
    pattern: "-(으)ㄴ/는 탓에",
    meaning: "表示將負面結果歸因於前項，相當於「都怪、由於」。",
    examples: [
      ["준비가 부족한 탓에 좋은 결과를 얻지 못했습니다.", "由於準備不足，沒能得到好結果。"],
      ["잠을 못 잔 탓에 하루 종일 피곤했습니다.", "因為沒睡好，一整天都很累。"]
    ]
  },
  {
    pattern: "-(으)ㄹ수록",
    meaning: "表示程度隨前項增加，相當於「越...越...」。",
    examples: [
      ["한국어는 공부할수록 재미있습니다.", "韓文越學越有趣。"],
      ["생각하면 할수록 어려운 문제입니다.", "這是越想越困難的問題。"]
    ]
  },
  {
    pattern: "-더라도",
    meaning: "表示讓步，相當於「即使...也...」。",
    examples: [
      ["힘들더라도 끝까지 포기하지 마세요.", "即使辛苦，也請不要放棄到最後。"],
      ["비가 오더라도 행사는 예정대로 진행됩니다.", "即使下雨，活動仍會照常進行。"]
    ]
  },
  {
    pattern: "-고자",
    meaning: "書面語，表示行動目的，相當於「為了、想要」。",
    examples: [
      ["문제를 해결하고자 전문가를 찾아갔습니다.", "為了解決問題，去找了專家。"],
      ["의견을 듣고자 설문 조사를 실시했습니다.", "為了聽取意見，進行了問卷調查。"]
    ]
  },
  {
    pattern: "-는 셈이다",
    meaning: "表示根據情況作出的判斷，相當於「等於、算是」。",
    examples: [
      ["매일 한 시간씩 공부하니 일주일에 일곱 시간을 공부하는 셈입니다.", "每天學一小時，等於一週學七小時。"],
      ["할인을 받았으니 배송비는 무료인 셈입니다.", "因為有折扣，等於免運費。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 리가 없다",
    meaning: "表示強烈否定某種可能性，相當於「不可能」。",
    examples: [
      ["그 사람이 약속을 잊을 리가 없습니다.", "那個人不可能忘記約定。"],
      ["이렇게 쉬운 문제가 틀릴 리가 없습니다.", "這麼簡單的題目不可能答錯。"]
    ]
  },
  {
    pattern: "-다 보니",
    meaning: "表示持續某行為後自然產生結果，相當於「做著做著就」。",
    examples: [
      ["매일 연습하다 보니 발음이 좋아졌습니다.", "每天練習之後，發音自然變好了。"],
      ["오랫동안 함께 일하다 보니 서로를 잘 이해하게 되었습니다.", "長期一起工作後，變得很了解彼此。"]
    ]
  }
];

function pickByDate(items, count, offset = 0) {
  const day = Math.floor(Date.now() / 86400000) + offset;
  const start = (day * count) % items.length;
  return Array.from({ length: count }, (_, index) => items[(start + index) % items.length]);
}

async function fetchFinanceHeadlines() {
  const urls = (process.env.FINANCE_NEWS_RSS_URLS || "")
    .split(",")
    .map((url) => url.trim())
    .filter(Boolean);

  const titles = [];
  for (const url of urls.slice(0, 4)) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(5000) });
      if (!response.ok) continue;
      const xml = await response.text();
      const matches = [...xml.matchAll(/<title><!\[CDATA\[(.*?)\]\]><\/title>|<title>(.*?)<\/title>/g)];
      for (const match of matches.slice(1, 4)) {
        const title = decodeXml(match[1] || match[2] || "").trim();
        if (title && !titles.includes(title)) titles.push(title);
      }
    } catch {
      continue;
    }
  }
  return titles.slice(0, 6);
}

function decodeXml(value) {
  return value
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'");
}

function vocabBubble(item, index) {
  return {
    type: "bubble",
    size: "mega",
    header: {
      type: "box",
      layout: "vertical",
      backgroundColor: "#2F7D6D",
      paddingAll: "16px",
      contents: [
        {
          type: "text",
          text: `TOPIK ${item.level} | DAY WORD ${String(index + 1).padStart(2, "0")}`,
          color: "#D9F7EF",
          size: "xs",
          weight: "bold"
        },
        {
          type: "text",
          text: item.word,
          color: "#FFFFFF",
          size: "xxl",
          weight: "bold",
          margin: "sm",
          wrap: true
        }
      ]
    },
    body: {
      type: "box",
      layout: "vertical",
      spacing: "md",
      paddingAll: "18px",
      contents: [
        {
          type: "box",
          layout: "baseline",
          spacing: "sm",
          contents: [
            { type: "text", text: item.pos, color: "#2F7D6D", size: "sm", weight: "bold", flex: 0 },
            { type: "text", text: item.translation, color: "#202832", size: "lg", weight: "bold", wrap: true }
          ]
        },
        { type: "separator", margin: "md" },
        {
          type: "text",
          text: item.exampleKo,
          color: "#202832",
          size: "md",
          wrap: true,
          margin: "md"
        },
        {
          type: "text",
          text: item.exampleZh || item.definitionZh,
          color: "#697386",
          size: "sm",
          wrap: true
        },
        {
          type: "text",
          text: "資料來源：韓國國立國語院 韓國語基礎辭典",
          color: "#9AA3AF",
          size: "xxs",
          wrap: true,
          margin: "lg"
        }
      ]
    }
  };
}

function grammarBubble(item, index) {
  return {
    type: "bubble",
    size: "mega",
    header: {
      type: "box",
      layout: "vertical",
      backgroundColor: "#7957C8",
      paddingAll: "16px",
      contents: [
        {
          type: "text",
          text: `GRAMMAR ${index + 1}`,
          color: "#EEE8FF",
          size: "xs",
          weight: "bold"
        },
        {
          type: "text",
          text: item.pattern,
          color: "#FFFFFF",
          size: "xl",
          weight: "bold",
          margin: "sm",
          wrap: true
        }
      ]
    },
    body: {
      type: "box",
      layout: "vertical",
      spacing: "md",
      paddingAll: "18px",
      contents: [
        {
          type: "text",
          text: item.meaning,
          color: "#202832",
          size: "md",
          wrap: true
        },
        { type: "separator", margin: "md" },
        ...item.examples.flatMap(([sentence, sentenceZh], exampleIndex) => [
          {
            type: "text",
            text: `例句 ${exampleIndex + 1}`,
            color: "#7957C8",
            size: "xs",
            weight: "bold",
            margin: exampleIndex === 0 ? "md" : "lg"
          },
          {
            type: "text",
            text: sentence,
            color: "#202832",
            size: "md",
            wrap: true
          },
          {
            type: "text",
            text: sentenceZh,
            color: "#697386",
            size: "sm",
            wrap: true
          }
        ])
      ]
    }
  };
}

function flexCarousel(altText, bubbles) {
  return {
    type: "flex",
    altText,
    contents: {
      type: "carousel",
      contents: bubbles
    }
  };
}

export async function financeMessages() {
  const headlines = await fetchFinanceHeadlines();
  const bullets = headlines.length ? headlines : financeFallback;
  const text = [
    "今日國際財金晨報",
    "",
    ...bullets.map((item, index) => `${index + 1}. ${item}`),
    "",
    "金融業觀察：留意利率、匯率、風險資產波動與客戶資產配置需求。",
    "合規提醒：本內容為資訊整理，非投資建議。"
  ].join("\n");
  return [textMessage(text)];
}

export function koreanVocabRows() {
  return pickByDate(topikVocab, 10).map((item) => ({
    word: item.w,
    level: item.l,
    pos: item.p,
    translation: item.t || item.d || "詞義整理中",
    definitionZh: item.d || "例句翻譯整理中",
    exampleKo: item.e || `오늘의 단어는 '${item.w}'입니다.`,
    exampleZh: ""
  }));
}

export function koreanVocabMessages(rows = koreanVocabRows()) {
  return [
    flexCarousel("今日韓檢 TOPIK 單字 1-5", rows.slice(0, 5).map(vocabBubble)),
    flexCarousel("今日韓檢 TOPIK 單字 6-10", rows.slice(5, 10).map((row, index) => vocabBubble(row, index + 5)))
  ];
}

export function koreanGrammarMessages() {
  const rows = pickByDate(grammarBank, 2, 1);
  return [flexCarousel("今日韓檢 TOPIK 文法 2 個", rows.map(grammarBubble))];
}

export async function preview(kind) {
  if (kind === "finance") return financeMessages();
  if (kind === "korean-vocab") return koreanVocabMessages();
  if (kind === "korean-grammar") return koreanGrammarMessages();
  throw new Error(`Unknown preview kind: ${kind}`);
}
