import topikVocab from "../data/topik-vocab.json" with { type: "json" };
import topikGrammar from "../data/topik-grammar.json" with { type: "json" };

export const TOPIK_VOCAB_COUNT = topikVocab.length;
export const TOPIK_GRAMMAR_COUNT = topikGrammar.length;

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
    pattern: "-(으)러 가다",
    attachment: "動詞語幹 + (으)러 가다/오다；有收音用 으러，無收音用 러。",
    meaning: "表示移動的目的，相當於「去／來做某事」。",
    examples: [
      ["친구를 만나러 카페에 갑니다.", "我去咖啡廳見朋友。"],
      ["책을 사러 서점에 갔어요.", "我去書店買書了。"]
    ]
  },
  {
    pattern: "-기 전에",
    attachment: "動詞語幹 + 기 전에；名詞 + 전에。",
    meaning: "表示某動作或時間之前，相當於「在...之前」。",
    examples: [
      ["밥을 먹기 전에 손을 씻으세요.", "吃飯前請洗手。"],
      ["시험을 보기 전에 복습을 했습니다.", "考試前我複習了。"]
    ]
  },
  {
    pattern: "-(으)ㄴ 후에",
    attachment: "動詞語幹 + (으)ㄴ 후에；有收音用 은 후에，無收音用 ㄴ 후에。",
    meaning: "表示前一動作完成之後，相當於「...之後」。",
    examples: [
      ["숙제를 한 후에 텔레비전을 봤어요.", "做完作業後看了電視。"],
      ["회의가 끝난 후에 점심을 먹었습니다.", "會議結束後吃了午餐。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 때",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 때；有收音用 을 때，無收音用 ㄹ 때。",
    meaning: "表示某個時間或情況，相當於「當...的時候」。",
    examples: [
      ["비가 올 때 우산을 가지고 가세요.", "下雨的時候請帶傘。"],
      ["한국어를 공부할 때 사전을 자주 봅니다.", "學韓文時我常查字典。"]
    ]
  },
  {
    pattern: "-(으)면",
    attachment: "動詞／形容詞語幹 + (으)면；有收音用 으면，無收音用 면。",
    meaning: "表示條件或假設，相當於「如果...就...」。",
    examples: [
      ["시간이 있으면 같이 커피를 마셔요.", "如果有時間，就一起喝咖啡吧。"],
      ["날씨가 좋으면 산책하러 갈 거예요.", "如果天氣好，我會去散步。"]
    ]
  },
  {
    pattern: "-아/어서",
    attachment: "動詞／形容詞語幹 + 아/어서，依母音選擇 아서 或 어서。",
    meaning: "表示原因或動作先後，相當於「因為...／先...再...」。",
    examples: [
      ["길이 막혀서 약속에 늦었어요.", "因為塞車，所以約會遲到了。"],
      ["집에 가서 저녁을 먹을 거예요.", "我要回家後吃晚餐。"]
    ]
  },
  {
    pattern: "-(으)니까",
    attachment: "動詞／形容詞語幹 + (으)니까；有收音用 으니까，無收音用 니까。",
    meaning: "表示原因、理由或發現，相當於「因為...」。",
    examples: [
      ["비가 오니까 창문을 닫으세요.", "因為下雨，請關窗戶。"],
      ["시간이 없으니까 택시를 탑시다.", "因為沒時間，我們搭計程車吧。"]
    ]
  },
  {
    pattern: "-지만",
    attachment: "動詞／形容詞語幹 + 지만。",
    meaning: "表示轉折，相當於「雖然...但是...」。",
    examples: [
      ["이 음식은 맵지만 맛있어요.", "這道菜雖然辣，但是很好吃。"],
      ["피곤하지만 숙제를 해야 합니다.", "雖然累，但必須做作業。"]
    ]
  },
  {
    pattern: "-(으)면서",
    attachment: "動詞語幹 + (으)면서；有收音用 으면서，無收音用 면서。",
    meaning: "表示兩個動作同時進行，相當於「一邊...一邊...」。",
    examples: [
      ["음악을 들으면서 공부합니다.", "我一邊聽音樂一邊讀書。"],
      ["친구와 이야기하면서 걸었어요.", "我一邊和朋友聊天一邊走路。"]
    ]
  },
  {
    pattern: "-거나",
    attachment: "動詞／形容詞語幹 + 거나。",
    meaning: "表示選擇，相當於「或者...」。",
    examples: [
      ["주말에는 영화를 보거나 책을 읽어요.", "週末我看電影或看書。"],
      ["바쁘면 전화하거나 메시지를 보내세요.", "如果忙，可以打電話或傳訊息。"]
    ]
  },
  {
    pattern: "-기 때문에",
    attachment: "動詞／形容詞語幹 + 기 때문에；名詞 + 때문에。",
    meaning: "表示原因，相當於「因為...」。",
    examples: [
      ["시험이 있기 때문에 일찍 자야 해요.", "因為有考試，所以必須早點睡。"],
      ["눈이 많이 오기 때문에 길이 미끄러워요.", "因為下很多雪，路很滑。"]
    ]
  },
  {
    pattern: "-는 것",
    attachment: "動詞語幹 + 는 것。",
    meaning: "把動作名詞化，相當於「做...這件事」。",
    examples: [
      ["매일 운동하는 것은 건강에 좋아요.", "每天運動對健康很好。"],
      ["한국어를 배우는 것이 재미있습니다.", "學韓文很有趣。"]
    ]
  },
  {
    pattern: "-기",
    attachment: "動詞／形容詞語幹 + 기。",
    meaning: "將動作或狀態名詞化，常用於標題、清單或固定表達。",
    examples: [
      ["일찍 일어나기가 쉽지 않아요.", "早起不容易。"],
      ["한국어 말하기를 연습하고 있어요.", "我正在練習說韓文。"]
    ]
  },
  {
    pattern: "-(으)ㄴ 적이 있다",
    attachment: "動詞語幹 + (으)ㄴ 적이 있다；有收音用 은 적，無收音用 ㄴ 적。",
    meaning: "表示曾經有過某經驗，相當於「曾經...」。",
    examples: [
      ["제주도에 간 적이 있어요.", "我曾經去過濟州島。"],
      ["한국 음식을 만든 적이 있습니다.", "我曾經做過韓國料理。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 테니까",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 테니까；有收音用 을 테니까，無收音用 ㄹ 테니까。",
    meaning: "表示說話者的推測、意志或前提，相當於「因為會...所以...」。",
    examples: [
      ["제가 먼저 갈 테니까 천천히 오세요.", "我會先去，所以你慢慢來。"],
      ["길이 막힐 테니까 일찍 출발합시다.", "路上可能會塞車，所以我們早點出發吧。"]
    ]
  },
  {
    pattern: "-는 동안",
    attachment: "動詞語幹 + 는 동안；名詞 + 동안。",
    meaning: "表示某段時間內，相當於「在...期間」。",
    examples: [
      ["친구를 기다리는 동안 책을 읽었어요.", "等朋友的期間我看了書。"],
      ["방학 동안 한국어를 열심히 공부했습니다.", "放假期間我認真學了韓文。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 만하다",
    attachment: "動詞語幹 + (으)ㄹ 만하다；有收音用 을 만하다，無收音用 ㄹ 만하다。",
    meaning: "表示值得做或程度可以接受，相當於「值得...／還算...」。",
    examples: [
      ["이 영화는 한 번 볼 만해요.", "這部電影值得看一次。"],
      ["그 식당은 가격도 괜찮고 가 볼 만합니다.", "那間餐廳價格也不錯，值得去看看。"]
    ]
  },
  {
    pattern: "-(으)ㄴ/는 척하다",
    attachment: "動詞現在形 + 는 척하다；動詞過去形 + (으)ㄴ 척하다；形容詞 + (으)ㄴ 척하다。",
    meaning: "表示假裝某種行為或狀態，相當於「假裝...」。",
    examples: [
      ["그는 모르는 척했어요.", "他裝作不知道。"],
      ["아이는 자는 척하고 있었어요.", "孩子正在裝睡。"]
    ]
  },
  {
    pattern: "-는 한",
    attachment: "動詞語幹 + 는 한。",
    meaning: "表示在某條件持續成立的範圍內，相當於「只要...就...」。",
    examples: [
      ["포기하지 않는 한 기회는 있습니다.", "只要不放棄，就還有機會。"],
      ["약속을 지키는 한 서로 믿을 수 있어요.", "只要遵守約定，就能彼此信任。"]
    ]
  },
  {
    pattern: "-는 이상",
    attachment: "動詞語幹 + 는 이상；形容詞語幹 + (으)ㄴ 이상。",
    meaning: "表示既然前提已成立，後項也應成立，相當於「既然...就...」。",
    examples: [
      ["시작한 이상 끝까지 해야 합니다.", "既然開始了，就應該做到最後。"],
      ["약속한 이상 꼭 지켜야 해요.", "既然約好了，就一定要遵守。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 성싶다",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 성싶다；有收音用 을 성싶다，無收音用 ㄹ 성싶다。",
    meaning: "表示說話者的推測，相當於「看來可能...」。",
    examples: [
      ["오늘은 비가 올 성싶어요.", "今天看來可能會下雨。"],
      ["그 일은 쉽게 끝날 성싶지 않습니다.", "那件事看來不太可能輕易結束。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 터이다",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 터이다；有收音用 을 터이다，無收音用 ㄹ 터이다。",
    meaning: "表示說話者的意志、打算或推測，相當於「會...、打算...」。",
    examples: [
      ["내일 회의 자료는 제가 준비할 터입니다.", "明天的會議資料我會準備。"],
      ["길이 막힐 터이니 조금 일찍 출발합시다.", "路上應該會塞車，所以我們早點出發吧。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 따름이다",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 따름이다；有收音用 을 따름이다，無收音用 ㄹ 따름이다。",
    meaning: "表示只有某種想法、狀態或行為，相當於「只是...而已」。",
    examples: [
      ["저는 사실을 말했을 따름입니다.", "我只是說了事實而已。"],
      ["도와주셔서 감사할 따름입니다.", "得到您的幫助，我只有感謝。"]
    ]
  },
  {
    pattern: "-하고",
    attachment: "名詞 + 하고。",
    meaning: "表示並列或共同對象，相當於「和...」。",
    examples: [
      ["저는 친구하고 영화를 봤어요.", "我和朋友看了電影。"],
      ["빵하고 우유를 샀습니다.", "我買了麵包和牛奶。"]
    ]
  },
  {
    pattern: "-도",
    attachment: "名詞 + 도。",
    meaning: "表示包含或追加，相當於「也」。",
    examples: [
      ["저도 한국어를 공부해요.", "我也學韓文。"],
      ["오늘은 커피도 마시고 차도 마셨어요.", "今天咖啡也喝了，茶也喝了。"]
    ]
  },
  {
    pattern: "-만",
    attachment: "名詞／數量詞 + 만。",
    meaning: "表示限定，相當於「只有、只」。",
    examples: [
      ["오늘은 회의가 하나만 있어요.", "今天只有一個會議。"],
      ["저는 아침에 커피만 마셨어요.", "我早上只喝了咖啡。"]
    ]
  },
  {
    pattern: "-는 중이다",
    attachment: "動詞語幹 + 는 중이다；名詞 + 중이다。",
    meaning: "表示動作正在進行，相當於「正在...」。",
    examples: [
      ["지금 회의를 하는 중입니다.", "現在正在開會。"],
      ["저는 점심을 먹는 중이에요.", "我正在吃午餐。"]
    ]
  },
  {
    pattern: "-자마자",
    attachment: "動詞語幹 + 자마자。",
    meaning: "表示前一動作一發生，後一動作立刻發生，相當於「一...就...」。",
    examples: [
      ["집에 도착하자마자 잠이 들었어요.", "一到家就睡著了。"],
      ["수업이 끝나자마자 도서관에 갔습니다.", "課一結束就去了圖書館。"]
    ]
  },
  {
    pattern: "-(으)ㄴ/는 줄 알다",
    attachment: "動詞現在形 + 는 줄 알다；動詞過去形／形容詞 + (으)ㄴ 줄 알다。",
    meaning: "表示以為或知道某事實，相當於「以為...／知道...」。",
    examples: [
      ["저는 오늘이 월요일인 줄 알았어요.", "我以為今天是星期一。"],
      ["그 사람이 이미 떠난 줄 알았습니다.", "我以為那個人已經離開了。"]
    ]
  },
  {
    pattern: "-(으)ㄴ/는 모양이다",
    attachment: "動詞現在形 + 는 모양이다；動詞過去形／形容詞 + (으)ㄴ 모양이다。",
    meaning: "表示根據情況推測，相當於「看樣子...」。",
    examples: [
      ["밖이 조용한 걸 보니 모두 잠든 모양이에요.", "看外面很安靜，大家好像都睡了。"],
      ["사람들이 우산을 쓰고 있는 걸 보니 비가 오는 모양입니다.", "看到人們撐傘，看樣子正在下雨。"]
    ]
  },
  {
    pattern: "-는 한편",
    attachment: "動詞語幹 + 는 한편；形容詞語幹 + (으)ㄴ 한편。",
    meaning: "表示同時具有兩個面向，相當於「一方面...另一方面...」。",
    examples: [
      ["그 회사는 비용을 줄이는 한편 품질을 높이고 있습니다.", "那家公司一方面降低成本，一方面提升品質。"],
      ["이 도시는 전통을 지키는 한편 새로운 문화를 받아들입니다.", "這座城市一方面保留傳統，一方面接受新文化。"]
    ]
  },
  {
    pattern: "-는 데 비해",
    attachment: "動詞語幹 + 는 데 비해；形容詞語幹 + (으)ㄴ 데 비해。",
    meaning: "表示比較基準，相當於「和...相比」。",
    examples: [
      ["가격이 비싼 데 비해 품질은 좋지 않아요.", "和價格昂貴相比，品質並不好。"],
      ["그는 나이가 어린 데 비해 생각이 깊습니다.", "他和年紀小相比，想法很成熟。"]
    ]
  },
  {
    pattern: "-(으)ㄹ 뿐이다",
    attachment: "動詞／形容詞語幹 + (으)ㄹ 뿐이다；有收音用 을 뿐이다，無收音用 ㄹ 뿐이다。",
    meaning: "表示除此之外沒有其他，相當於「只是...而已」。",
    examples: [
      ["저는 해야 할 일을 했을 뿐입니다.", "我只是做了該做的事而已。"],
      ["그 말은 제 의견일 뿐이에요.", "那句話只是我的意見而已。"]
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
  },
  {
    level: 2,
    pattern: "-아/어 보다",
    attachment: "動詞語幹 + 아/어 보다。",
    meaning: "表示嘗試做某事，相當於「試著...」。",
    examples: [
      ["이 방법으로 다시 한번 해 보세요.", "請用這個方法再試一次。"],
      ["시간이 있으면 그 식당에 가 보려고 해요.", "如果有時間，我想去那間餐廳試試看。"]
    ]
  },
  {
    level: 2,
    pattern: "-고 있다",
    attachment: "動詞語幹 + 고 있다。",
    meaning: "表示動作正在進行或狀態持續，相當於「正在...」。",
    examples: [
      ["저는 지금 회의 자료를 정리하고 있어요.", "我現在正在整理會議資料。"],
      ["동생은 방에서 숙제를 하고 있습니다.", "弟弟正在房間裡寫作業。"]
    ]
  },
  {
    level: 2,
    pattern: "-아/어야 하다",
    attachment: "動詞 / 形容詞語幹 + 아/어야 하다。",
    meaning: "表示必須做某事，相當於「應該...、必須...」。",
    examples: [
      ["내일 일찍 출근해야 해서 오늘은 빨리 잘 거예요.", "明天必須早點上班，所以今天要早點睡。"],
      ["시험 전에는 단어를 꼭 복습해야 해요.", "考試前一定要複習單字。"]
    ]
  },
  {
    level: 2,
    pattern: "-아/어도 되다",
    attachment: "動詞語幹 + 아/어도 되다。",
    meaning: "表示允許或可以做某事，相當於「可以...」。",
    examples: [
      ["여기 앉아도 돼요?", "我可以坐這裡嗎？"],
      ["회의가 끝나면 먼저 가도 됩니다.", "會議結束後可以先離開。"]
    ]
  },
  {
    level: 2,
    pattern: "-(으)면 안 되다",
    attachment: "動詞語幹有收音用 으면 안 되다，無收音用 면 안 되다。",
    meaning: "表示禁止做某事，相當於「不可以...」。",
    examples: [
      ["도서관에서는 크게 말하면 안 돼요.", "在圖書館不可以大聲說話。"],
      ["중요한 파일은 함부로 지우면 안 됩니다.", "重要檔案不可以隨便刪除。"]
    ]
  },
  {
    level: 3,
    pattern: "-(으)려고 하다",
    attachment: "動詞語幹有收音用 으려고 하다，無收音用 려고 하다。",
    meaning: "表示打算或準備做某事，相當於「想要...、打算...」。",
    examples: [
      ["퇴근 후에 친구를 만나려고 해요.", "下班後我打算見朋友。"],
      ["이번 주말에는 집에서 쉬려고 합니다.", "這週末我打算在家休息。"]
    ]
  },
  {
    level: 2,
    pattern: "-(으)러 오다",
    attachment: "動詞語幹有收音用 으러 오다，無收音用 러 오다。",
    meaning: "表示來的目的，相當於「來...」。",
    examples: [
      ["친구가 저를 만나러 회사 근처에 왔어요.", "朋友來公司附近找我。"],
      ["학생들이 한국어를 배우러 교실에 왔습니다.", "學生們來教室學韓文。"]
    ]
  },
  {
    level: 3,
    pattern: "-고 나서",
    attachment: "動詞語幹 + 고 나서。",
    meaning: "表示前一動作完成後再做後一動作，相當於「...之後」。",
    examples: [
      ["회의가 끝나고 나서 결과를 메일로 보냈어요.", "會議結束後，我用信件寄出了結果。"],
      ["저녁을 먹고 나서 산책을 했습니다.", "吃完晚餐後去散步了。"]
    ]
  },
  {
    level: 2,
    pattern: "-아/어 주다",
    attachment: "動詞語幹 + 아/어 주다。",
    meaning: "表示為別人做某事，相當於「幫...」。",
    examples: [
      ["친구가 지하철역 가는 길을 찾아 줬어요.", "朋友幫我找到了去捷運站的路。"],
      ["동료가 회의실 문을 열어 줬어요.", "同事幫我打開了會議室的門。"]
    ]
  },
  {
    level: 3,
    pattern: "-(으)ㄴ 것 같다",
    attachment: "動詞過去形 / 形容詞語幹 + (으)ㄴ 것 같다。",
    meaning: "表示推測，相當於「好像...」。",
    examples: [
      ["밖이 조용한 걸 보니 회의가 끝난 것 같아요.", "看外面很安靜，會議好像結束了。"],
      ["표정을 보니 기분이 좋은 것 같습니다.", "看表情，心情好像不錯。"]
    ]
  }
];

const TOPIK_LEVELS = [1, 2, 3, 4, 5, 6];
const BLOCKED_VOCAB_WORDS = new Set(["구도", "이", "다", "한", "도", "어", "나", "지", "무", "삼"]);
const CURATED_VOCAB_WORDS = new Set([
  "학교", "친구", "시간", "음식", "회의", "준비하다", "끝나다", "약속", "방법", "건강",
  "은행", "병원", "회사원", "직장", "점심", "저녁", "버스", "날씨", "옷", "커피",
  "가게", "교실", "거리", "나라", "물건", "선물", "질문", "책상", "침대", "휴일",
  "노래", "운전", "휴대폰", "뉴스",
  "장갑", "막다", "명단", "백팔십도", "추모하다", "운동", "한두", "결과적", "보급", "민주화되다",
  "한계", "떼이다", "패배하다", "꼭", "메모하다", "관계하다", "돼지꿈", "매력적", "공단", "가격",
  "번역어", "광산", "넣다", "깎다", "큰집", "맞서다", "실거래", "구도", "높다", "속옷",
  "붕괴", "김", "약하다", "머리하다", "뼈", "독립적", "호소", "얘기하다", "여권", "살구",
  "위로하다", "정권", "항복", "책", "공개", "보급하다", "논란", "통로", "회사", "다녀오다",
  "검토하다", "무가치하다", "침해", "역시", "화요일", "그녀", "계시되다", "입법", "넘다", "그러므로",
  "뜻하다", "위로되다", "오래달리기", "믿다", "외국어", "관계없다", "매번", "입문", "삼", "평일",
  "듣기", "보급되다", "이", "다", "하다", "한", "도", "있다", "어", "일",
  "나", "지", "주거하다", "무", "글쎄요", "확인되다", "팁", "계시하다", "처형되다", "얘기",
  "갚다", "막", "접근법", "저리되다", "괜찮다", "셋째", "첫사랑", "실망시키다", "회원제", "저리하다",
  "드리다", "시골", "손님", "없이", "악화", "가끔가다가", "저리다", "안녕하다", "택배", "첫차",
  "고급화", "민주화하다", "나라님", "긍정적", "계시", "치명적", "의미하다", "낚시하다", "별생각", "돼지머리",
  "값있다", "눌러앉다", "악화되다", "값하다", "압도되다", "하루", "글쎄", "인간적", "악화하다", "꽃답다",
  "압도하다", "언제", "새사람", "에이", "죽어지내다", "타격하다", "여러분", "검정색", "관계있다", "위로",
  "하늘거리다", "특유하다", "신규", "염려", "연결", "연극", "연관", "연간", "도달하다", "애초",
  "답", "연락처", "테니스", "관련되다", "검토되다", "큰아기", "업소", "운동하다", "삼촌", "질"
]);

function excludedValues(name) {
  const value = globalThis.process?.env?.[name] || globalThis[name] || "";
  return new Set(String(value).split(/\n|,/).map((item) => item.trim()).filter(Boolean));
}

function dayNumber(offset = 0) {
  const overrideDate = globalThis.process?.env?.HANHAN_DATE || globalThis.HANHAN_DATE;
  const values = overrideDate
    ? { year: overrideDate.slice(0, 4), month: overrideDate.slice(5, 7), day: overrideDate.slice(8, 10) }
    : Object.fromEntries(new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Taipei",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).formatToParts(new Date()).map((part) => [part.type, part.value]));
  const taipeiMidnightUtc = Date.UTC(Number(values.year), Number(values.month) - 1, Number(values.day));
  return Math.floor(taipeiMidnightUtc / 86400000) + offset;
}

function levelSlotsForDay(day, count) {
  const start = day % TOPIK_LEVELS.length;
  return Array.from({ length: count }, (_, index) => TOPIK_LEVELS[(start + index) % TOPIK_LEVELS.length]);
}

function countLevelSlotsBeforeDay(day, count, level) {
  const fullCycles = Math.floor(day / TOPIK_LEVELS.length);
  const remainingDays = day % TOPIK_LEVELS.length;
  let total = fullCycles * count;
  for (let dayOffset = 0; dayOffset < remainingDays; dayOffset += 1) {
    total += levelSlotsForDay(dayOffset, count).filter((slotLevel) => slotLevel === level).length;
  }
  return total;
}

function groupByLevel(items, levelKey) {
  return items.reduce((groups, item) => {
    const level = Number(item[levelKey]);
    if (!groups.has(level)) groups.set(level, []);
    groups.get(level).push(item);
    return groups;
  }, new Map());
}

function pickByDateAcrossLevels(items, count, levelKey, offset = 0) {
  const day = dayNumber(offset);
  const groups = groupByLevel(items, levelKey);
  const pickedByLevel = new Map();
  const pickedKeys = new Set();
  const itemKey = (item) => item.w || item.pattern || JSON.stringify(item);
  return levelSlotsForDay(day, count).map((level) => {
    const group = (groups.get(level) || []).filter((item) => !pickedKeys.has(itemKey(item)));
    const fallback = items.filter((item) => !pickedKeys.has(itemKey(item)));
    const candidates = group.length ? group : fallback.length ? fallback : (groups.get(level) || items);
    const pickedToday = pickedByLevel.get(level) || 0;
    const index = (countLevelSlotsBeforeDay(day, count, level) + pickedToday) % candidates.length;
    const item = candidates[index];
    pickedByLevel.set(level, pickedToday + 1);
    pickedKeys.add(itemKey(item));
    return item;
  });
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
          text: `TOPIK ${item.level} | GRAMMAR ${index + 1}`,
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
          text: item.attachment || "接續規則依詞性與時態調整。",
          color: "#202832",
          size: "sm",
          wrap: true
        },
        {
          type: "text",
          text: item.meaning || "此文法的詳細說明整理中。",
          color: "#202832",
          size: "md",
          wrap: true
        },
        { type: "separator", margin: "md" },
        ...(item.examples || []).flatMap(([sentence, sentenceZh], exampleIndex) => [
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
  const exampleZhByWord = {
    "나라님": "在古老故事裡，百姓們尊敬國君。",
    "긍정적": "主管對我的提案表現出正面的反應。",
    "계시": "他在困難時期像得到啟示一樣，心情變得平靜。",
    "치명적": "小小的失誤也可能成為專案中的致命問題。",
    "의미하다": "這個標示表示會議室不能使用。",
    "낚시하다": "週末我和爸爸在河邊釣魚。",
    "별생각": "一開始我沒想太多就進了會議。",
    "돼지머리": "開幕儀式時，桌上放了豬頭。",
    "값있다": "失敗的經驗後來也成了寶貴的學習。",
    "눌러앉다": "我只是去朋友家一下，結果一直待到晚上。"
  };
  const excludedWords = excludedValues("HANHAN_EXCLUDE_VOCAB_WORDS");
  const curatedVocab = topikVocab.filter((item) =>
    CURATED_VOCAB_WORDS.has(item.w) &&
    !BLOCKED_VOCAB_WORDS.has(item.w) &&
    !excludedWords.has(item.w)
  );
  return pickByDateAcrossLevels(curatedVocab.length ? curatedVocab : topikVocab, 10, "l").map((item) => ({
    word: item.w,
    level: item.l,
    pos: item.p,
    translation: item.t || item.d || "詞義整理中",
    definitionZh: item.d || "例句翻譯整理中",
    exampleKo: item.e || `오늘의 단어는 '${item.w}'입니다.`,
    exampleZh: exampleZhByWord[item.w] || ""
  }));
}

export function koreanVocabMessages(rows = koreanVocabRows()) {
  return [
    flexCarousel("今日韓檢 TOPIK 單字 1-5", rows.slice(0, 5).map(vocabBubble)),
    flexCarousel("今日韓檢 TOPIK 單字 6-10", rows.slice(5, 10).map((row, index) => vocabBubble(row, index + 5)))
  ];
}

export function koreanGrammarRows() {
  const levelByPattern = new Map(topikGrammar.map((item) => [item.pattern, item.level]));
  const excludedPatterns = excludedValues("HANHAN_EXCLUDE_GRAMMAR_PATTERNS");
  const completeGrammar = grammarBank
    .map((item) => ({ ...item, level: levelByPattern.get(item.pattern) || item.level }))
    .filter((item) =>
      item.level &&
      item.attachment &&
      item.meaning &&
      Array.isArray(item.examples) &&
      item.examples.length >= 2 &&
      !excludedPatterns.has(item.pattern)
    );
  return pickByDateAcrossLevels(completeGrammar, 2, "level", 1).map((item) => {
    return {
      level: item.level,
      pattern: item.pattern,
      attachment: item.attachment,
      meaning: item.meaning,
      examples: item.examples
    };
  });
}

export function koreanGrammarMessages(rows = koreanGrammarRows()) {
  return [flexCarousel("今日韓檢 TOPIK 文法 2 個", rows.map(grammarBubble))];
}

export async function preview(kind) {
  if (kind === "finance") return financeMessages();
  if (kind === "korean-vocab") return koreanVocabMessages();
  if (kind === "korean-grammar") return koreanGrammarMessages();
  throw new Error(`Unknown preview kind: ${kind}`);
}
