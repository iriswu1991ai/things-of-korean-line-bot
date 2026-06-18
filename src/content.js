function textMessage(text) {
  return { type: "text", text: text.slice(0, 5000) };
}

const financeFallback = [
  "美國利率預期與美元走勢仍是今日市場定價主軸。",
  "亞洲股匯市需留意科技股財報、資金輪動與央行官員談話。",
  "原油與黃金價格可作為通膨預期、避險需求與實質利率變化的觀察指標。",
  "金融業今日可聚焦授信曝險、外幣部位與客戶再平衡需求。"
];

const vocabBank = [
  ["경제", "經濟", "名詞", "세계 경제가 빠르게 변하고 있습니다.", "世界經濟正在快速變化。"],
  ["금리", "利率", "名詞", "금리가 오르면 대출 부담이 커집니다.", "利率上升時，貸款負擔會變大。"],
  ["환율", "匯率", "名詞", "환율 변동은 수출 기업에 영향을 줍니다.", "匯率變動會影響出口企業。"],
  ["증가하다", "增加", "動詞", "온라인 수업을 듣는 학생이 증가하고 있습니다.", "上線上課的學生正在增加。"],
  ["감소하다", "減少", "動詞", "출생률이 계속 감소하고 있습니다.", "出生率持續下降。"],
  ["분석하다", "分析", "動詞", "전문가는 자료를 자세히 분석했습니다.", "專家詳細分析了資料。"],
  ["정책", "政策", "名詞", "정부는 새로운 교육 정책을 발표했습니다.", "政府發表了新的教育政策。"],
  ["환경", "環境", "名詞", "환경 보호는 모두의 책임입니다.", "環境保護是所有人的責任。"],
  ["소비자", "消費者", "名詞", "소비자는 가격과 품질을 비교합니다.", "消費者會比較價格和品質。"],
  ["영향", "影響", "名詞", "스마트폰은 생활에 큰 영향을 미쳤습니다.", "智慧型手機對生活產生了很大的影響。"],
  ["지속적", "持續的", "冠形詞/名詞", "지속적인 노력이 필요합니다.", "需要持續的努力。"],
  ["개선하다", "改善", "動詞", "시는 교통 문제를 개선하려고 합니다.", "市政府想改善交通問題。"],
  ["복잡하다", "複雜", "形容詞", "이 문제는 생각보다 복잡합니다.", "這個問題比想像中複雜。"],
  ["가능성", "可能性", "名詞", "성공할 가능성이 높습니다.", "成功的可能性很高。"],
  ["제한하다", "限制", "動詞", "학교는 휴대폰 사용을 제한했습니다.", "學校限制了手機使用。"],
  ["참여하다", "參與", "動詞", "많은 시민이 행사에 참여했습니다.", "許多市民參與了活動。"],
  ["필수적", "必要的", "冠形詞/名詞", "외국어 능력은 취업에 필수적입니다.", "外語能力對就業是必要的。"],
  ["확대하다", "擴大", "動詞", "회사는 해외 투자를 확대했습니다.", "公司擴大了海外投資。"],
  ["비교하다", "比較", "動詞", "두 제품의 장단점을 비교해 보세요.", "請比較兩項產品的優缺點。"],
  ["원인", "原因", "名詞", "문제의 원인을 찾아야 합니다.", "必須找出問題的原因。"]
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

function vocabBubble([word, translation, pos, sentence, sentenceZh], index) {
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
          text: `DAY WORD ${String(index + 1).padStart(2, "0")}`,
          color: "#D9F7EF",
          size: "xs",
          weight: "bold"
        },
        {
          type: "text",
          text: word,
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
            { type: "text", text: pos, color: "#2F7D6D", size: "sm", weight: "bold", flex: 0 },
            { type: "text", text: translation, color: "#202832", size: "lg", weight: "bold", wrap: true }
          ]
        },
        { type: "separator", margin: "md" },
        {
          type: "text",
          text: sentence,
          color: "#202832",
          size: "md",
          wrap: true,
          margin: "md"
        },
        {
          type: "text",
          text: sentenceZh,
          color: "#697386",
          size: "sm",
          wrap: true
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

export function koreanVocabMessages() {
  const rows = pickByDate(vocabBank, 10);
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
