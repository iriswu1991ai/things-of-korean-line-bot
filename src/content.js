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
  ["원인", "原因", "名詞", "문제의 원인을 찾아야 합니다.", "必須找出問題的原因。"],
  ["결과", "結果", "名詞", "연구 결과가 다음 주에 발표됩니다.", "研究結果將於下週公布。"],
  ["현상", "現象", "名詞", "이러한 현상은 여러 나라에서 나타납니다.", "這種現象出現在許多國家。"],
  ["해결하다", "解決", "動詞", "대화를 통해 갈등을 해결해야 합니다.", "應該透過對話解決衝突。"],
  ["제공하다", "提供", "動詞", "도서관은 다양한 자료를 제공합니다.", "圖書館提供多樣的資料。"],
  ["발생하다", "發生", "動詞", "시스템 오류가 갑자기 발생했습니다.", "系統突然發生錯誤。"],
  ["요구하다", "要求", "動詞", "시민들은 더 안전한 환경을 요구했습니다.", "市民要求更安全的環境。"],
  ["이용하다", "利用、使用", "動詞", "대중교통을 이용하면 시간을 절약할 수 있습니다.", "使用大眾運輸可以節省時間。"],
  ["선택하다", "選擇", "動詞", "자신에게 맞는 방법을 선택하세요.", "請選擇適合自己的方法。"],
  ["조사", "調查", "名詞", "정부는 생활 만족도 조사를 실시했습니다.", "政府進行了生活滿意度調查。"],
  ["관계", "關係", "名詞", "신뢰는 인간관계에서 매우 중요합니다.", "信任在人際關係中非常重要。"],
  ["목표", "目標", "名詞", "구체적인 목표를 세우는 것이 좋습니다.", "最好設定具體的目標。"],
  ["조건", "條件", "名詞", "지원 조건을 미리 확인해 주세요.", "請事先確認申請條件。"],
  ["경험", "經驗", "名詞", "다양한 경험은 성장에 도움이 됩니다.", "多樣的經驗有助於成長。"],
  ["효과", "效果", "名詞", "규칙적인 운동은 스트레스 감소에 효과가 있습니다.", "規律運動具有減輕壓力的效果。"],
  ["과정", "過程", "名詞", "결과보다 배우는 과정이 더 중요합니다.", "比起結果，學習的過程更重要。"],
  ["기준", "標準、基準", "名詞", "평가 기준이 명확해야 합니다.", "評價標準必須明確。"],
  ["변화", "變化", "名詞", "기술의 발전은 사회에 큰 변화를 가져왔습니다.", "科技發展為社會帶來巨大變化。"],
  ["주장", "主張", "名詞", "그의 주장은 충분한 근거가 있습니다.", "他的主張有充分的根據。"],
  ["태도", "態度", "名詞", "긍정적인 태도로 문제를 바라보세요.", "請以正面的態度看待問題。"],
  ["자료", "資料", "名詞", "발표에 필요한 자료를 정리했습니다.", "整理了發表所需的資料。"]
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
