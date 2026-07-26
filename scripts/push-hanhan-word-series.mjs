import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { loadEnv } from "../src/env.js";
import { broadcast, textMessage } from "../src/line.js";

const rootDir = resolve(dirname(fileURLToPath(import.meta.url)), "..");
loadEnv(resolve(rootDir, ".env"));

const statePath = resolve(rootDir, "data", "hanhan-word-series-state.json");

const GROUPS = [
  {
    key: "맛",
    words: [
      ["맛", "***", "味道"],
      ["맛있다", "***", "好吃"],
      ["맛없다", "***", "不好吃"],
      ["맛보다", "**", "品嘗"],
      ["맛집", "**", "美食店"],
      ["맛보기", "**", "試吃、預覽"],
      ["맛나다", "**", "好吃、有味道"],
      ["맛내다", "**", "調味、做出味道"],
      ["맛깔", "*", "風味、滋味"],
      ["맛소금", "*", "調味鹽"]
    ]
  },
  {
    key: "입",
    words: [
      ["입", "***", "嘴巴"],
      ["입구", "***", "入口"],
      ["입다", "***", "穿"],
      ["입장", "**", "入場、立場"],
      ["입학", "**", "入學"],
      ["입원", "**", "住院"],
      ["입금", "**", "匯款、入帳"],
      ["입맛", "**", "食慾、口味"],
      ["입사", "*", "進公司、入社"],
      ["입국", "*", "入境"]
    ]
  },
  {
    key: "눈",
    words: [
      ["눈", "***", "眼睛、雪"],
      ["눈물", "***", "眼淚"],
      ["눈사람", "***", "雪人"],
      ["눈길", "**", "目光、雪路"],
      ["눈빛", "**", "眼神"],
      ["눈앞", "**", "眼前"],
      ["눈치", "**", "眼色、察言觀色"],
      ["눈병", "**", "眼疾"],
      ["눈썹", "**", "眉毛"],
      ["눈높이", "*", "眼光、標準"]
    ]
  },
  {
    key: "손",
    words: [
      ["손", "***", "手"],
      ["손님", "***", "客人"],
      ["손가락", "***", "手指"],
      ["손목", "**", "手腕"],
      ["손잡이", "**", "把手"],
      ["손질", "**", "整理、修整"],
      ["손해", "**", "損害、虧損"],
      ["손수", "**", "親手"],
      ["손발", "*", "手腳"],
      ["손바닥", "*", "手掌"]
    ]
  },
  {
    key: "물",
    words: [
      ["물", "***", "水"],
      ["물건", "***", "物品、東西"],
      ["물고기", "***", "魚"],
      ["물어보다", "***", "問看看"],
      ["물론", "***", "當然"],
      ["물가", "**", "物價"],
      ["물질", "**", "物質"],
      ["물약", "**", "藥水"],
      ["물속", "*", "水中"],
      ["물음", "*", "問題、提問"]
    ]
  },
  {
    key: "마",
    words: [
      ["마음", "***", "心、心情"],
      ["마시다", "***", "喝"],
      ["마지막", "***", "最後"],
      ["마을", "***", "村子"],
      ["마늘", "**", "大蒜"],
      ["마치다", "**", "結束、完成"],
      ["마중", "**", "迎接"],
      ["마당", "**", "院子"],
      ["마감", "*", "截止、收尾"],
      ["마찰", "*", "摩擦"]
    ]
  },
  {
    key: "바",
    words: [
      ["바다", "***", "海"],
      ["바지", "***", "褲子"],
      ["바람", "***", "風"],
      ["바로", "***", "馬上、正是"],
      ["바쁘다", "***", "忙"],
      ["바꾸다", "***", "更換、改變"],
      ["바닥", "**", "地板、底部"],
      ["바깥", "**", "外面"],
      ["바탕", "*", "基礎、底子"],
      ["바늘", "*", "針"]
    ]
  },
  {
    key: "가",
    words: [
      ["가다", "***", "去"],
      ["가지다", "***", "擁有、拿"],
      ["가르치다", "***", "教"],
      ["가을", "***", "秋天"],
      ["가운데", "***", "中間"],
      ["가능", "**", "可能"],
      ["가득", "**", "滿滿地"],
      ["가입", "**", "加入"],
      ["가로", "*", "橫向"],
      ["가짜", "*", "假的"]
    ]
  },
  {
    key: "이",
    words: [
      ["이름", "***", "名字"],
      ["이야기", "***", "故事、談話"],
      ["이상", "***", "以上、異常"],
      ["이하", "**", "以下"],
      ["이유", "***", "理由"],
      ["이용", "**", "利用、使用"],
      ["이사", "**", "搬家"],
      ["이웃", "**", "鄰居"],
      ["이익", "*", "利益"],
      ["이별", "*", "離別"]
    ]
  },
  {
    key: "주",
    words: [
      ["주다", "***", "給"],
      ["주말", "***", "週末"],
      ["주문", "***", "點餐、訂購"],
      ["주소", "***", "地址"],
      ["주로", "**", "主要地"],
      ["주변", "**", "周邊"],
      ["주의", "**", "注意"],
      ["주제", "**", "主題"],
      ["주인", "**", "主人、老闆"],
      ["주차", "**", "停車"]
    ]
  },
  {
    key: "내",
    words: [
      ["내년", "***", "明年"],
      ["내일", "***", "明天"],
      ["내용", "**", "內容"],
      ["내다", "***", "交、出、繳"],
      ["내려가다", "**", "下去"],
      ["내려오다", "**", "下來"],
      ["내리다", "***", "下、降"],
      ["내부", "**", "內部"],
      ["내외", "*", "內外、左右"],
      ["내성적", "*", "內向的"]
    ]
  },
  {
    key: "외",
    words: [
      ["외국", "***", "外國"],
      ["외국인", "***", "外國人"],
      ["외출", "**", "外出"],
      ["외롭다", "**", "孤單"],
      ["외우다", "***", "背、記住"],
      ["외모", "**", "外貌"],
      ["외부", "**", "外部"],
      ["외과", "*", "外科"],
      ["외교", "*", "外交"],
      ["외식", "**", "外食、外出用餐"]
    ]
  },
  {
    key: "편",
    words: [
      ["편지", "***", "信"],
      ["편하다", "***", "舒服、方便"],
      ["편의점", "***", "便利商店"],
      ["편리", "**", "便利"],
      ["편안", "**", "平安、舒適"],
      ["편집", "**", "編輯"],
      ["편견", "*", "偏見"],
      ["편도", "*", "單程"],
      ["편식", "*", "偏食"],
      ["편명", "*", "航班號、班次名"]
    ]
  },
  {
    key: "운",
    words: [
      ["운동", "***", "運動"],
      ["운전", "***", "駕駛"],
      ["운명", "**", "命運"],
      ["운영", "**", "營運、經營"],
      ["운반", "**", "搬運"],
      ["운임", "*", "運費、車資"],
      ["운하", "*", "運河"],
      ["운세", "*", "運勢"],
      ["운전사", "**", "司機"],
      ["운동장", "**", "運動場"]
    ]
  },
  {
    key: "두",
    words: [
      ["두", "***", "兩個"],
      ["두다", "***", "放、擺"],
      ["두껍다", "**", "厚"],
      ["두렵다", "**", "害怕"],
      ["두통", "**", "頭痛"],
      ["두부", "**", "豆腐"],
      ["두근거리다", "**", "怦怦跳"],
      ["두드리다", "**", "敲、拍"],
      ["두뇌", "*", "頭腦"],
      ["두통약", "*", "頭痛藥"]
    ]
  },
  {
    key: "밤",
    words: [
      ["밤", "***", "晚上、栗子"],
      ["밤새", "**", "整夜"],
      ["밤낮", "**", "日夜"],
      ["밤길", "**", "夜路"],
      ["밤하늘", "**", "夜空"],
      ["밤중", "**", "半夜"],
      ["밤샘", "*", "熬夜"],
      ["밤비", "*", "夜雨"],
      ["밤공기", "*", "夜晚空氣"],
      ["밤거리", "*", "夜晚街道"]
    ]
  },
  {
    key: "김",
    words: [
      ["김", "***", "海苔、熱氣"],
      ["김치", "***", "泡菜"],
      ["김밥", "***", "紫菜飯捲"],
      ["김치찌개", "**", "泡菜鍋"],
      ["김장", "**", "醃泡菜"],
      ["김치전", "**", "泡菜煎餅"],
      ["김가루", "*", "海苔粉"],
      ["김치볶음밥", "**", "泡菜炒飯"],
      ["김치국", "*", "泡菜湯"],
      ["김말이", "*", "炸海苔粉絲捲"]
    ]
  },
  {
    key: "밥",
    words: [
      ["밥", "***", "飯"],
      ["밥집", "**", "飯館"],
      ["밥상", "**", "飯桌"],
      ["밥맛", "**", "飯味、食慾"],
      ["밥솥", "**", "飯鍋"],
      ["밥그릇", "**", "飯碗"],
      ["밥벌이", "*", "謀生"],
      ["밥값", "**", "飯錢"],
      ["밥알", "*", "飯粒"],
      ["밥때", "*", "飯點、吃飯時間"]
    ]
  },
  {
    key: "길",
    words: [
      ["길", "***", "路"],
      ["길다", "***", "長"],
      ["길거리", "**", "街上"],
      ["길이", "**", "長度"],
      ["길잡이", "*", "嚮導、指南"],
      ["길목", "*", "路口、要道"],
      ["길가", "**", "路邊"],
      ["길찾기", "**", "找路、導航"],
      ["길들이다", "*", "馴服、使習慣"],
      ["길어지다", "**", "變長"]
    ]
  },
  {
    key: "몸",
    words: [
      ["몸", "***", "身體"],
      ["몸무게", "***", "體重"],
      ["몸살", "**", "全身痠痛"],
      ["몸짓", "**", "肢體動作"],
      ["몸매", "**", "身材"],
      ["몸속", "**", "體內"],
      ["몸통", "*", "軀幹"],
      ["몸집", "*", "體格"],
      ["몸조리", "*", "調養身體"],
      ["몸 상태", "**", "身體狀態"]
    ]
  },
  {
    key: "책",
    words: [
      ["책", "***", "書"],
      ["책상", "***", "書桌"],
      ["책방", "**", "書店"],
      ["책임", "**", "責任"],
      ["책임자", "**", "負責人"],
      ["책갈피", "*", "書籤"],
      ["책장", "**", "書櫃、書頁"],
      ["책자", "*", "冊子、小書"],
      ["책임감", "**", "責任感"],
      ["책벌레", "*", "書蟲、愛書人"]
    ]
  },
  {
    key: "문",
    words: [
      ["문", "***", "門"],
      ["문밖", "**", "門外"],
      ["문앞", "**", "門前"],
      ["문손잡이", "**", "門把"],
      ["문틈", "*", "門縫"],
      ["문안", "*", "問安"],
      ["문턱", "*", "門檻"],
      ["문단속", "**", "鎖門、門戶管理"],
      ["문고리", "*", "門環、門把"],
      ["문지기", "*", "門衛"]
    ]
  }
];

function todayInTaipei() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Taipei",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date());
}

function minutesInTaipei() {
  const parts = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Taipei",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return Number(values.hour) * 60 + Number(values.minute);
}

function readState() {
  if (!existsSync(statePath)) {
    return { nextDay: 34, sentDates: {}, usedWords: [] };
  }
  return JSON.parse(readFileSync(statePath, "utf8"));
}

function writeState(state) {
  writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`, "utf8");
}

function formatPost(day, group) {
  const lines = [
    `不專業的一起背韓文單字 Day ${day}`,
    "（***韓文1-2급/**韓文3-4급/韓文5-6급）",
    "",
    ...group.words.map(([word, level, meaning]) => `${word} ${level} ${meaning}`)
  ];
  return lines.join("\n");
}

function validateGroup(group, usedWords) {
  if (group.words.length !== 10) return false;
  return group.words.every(([word]) => word.startsWith(group.key) && !usedWords.has(word));
}

const date = process.env.HANHAN_WORD_SERIES_DATE || todayInTaipei();
const isScheduledRun = process.env.GITHUB_EVENT_NAME === "schedule";
const requireMorning = process.env.HANHAN_WORD_SERIES_REQUIRE_TAIPEI_MORNING === "1" && isScheduledRun;
const minutes = minutesInTaipei();

if (requireMorning && minutes < 8 * 60) {
  console.log(`Skipped HANHAN word series: outside Taipei morning window at minute ${minutes}.`);
  process.exit(0);
}

const state = readState();
if (state.sentDates?.[date]) {
  console.log(`Skipped HANHAN word series: ${date} already sent as Day ${state.sentDates[date].day}.`);
  process.exit(0);
}

const usedWords = new Set(state.usedWords || []);
const group = GROUPS.find((candidate) => validateGroup(candidate, usedWords));

if (!group) {
  throw new Error("No unused HANHAN word-series group is available.");
}

const day = Number(state.nextDay || 34);
const text = formatPost(day, group);

if (process.env.DRY_RUN === "1") {
  console.log(text);
  process.exit(0);
}

if (!process.env.LINE_HANHAN_CHANNEL_ACCESS_TOKEN) {
  throw new Error("Missing LINE_HANHAN_CHANNEL_ACCESS_TOKEN.");
}

await broadcast("hanhan", [textMessage(text)]);

state.nextDay = day + 1;
state.sentDates = {
  ...(state.sentDates || {}),
  [date]: {
    day,
    key: group.key,
    words: group.words.map(([word]) => word),
    sentAt: new Date().toISOString()
  }
};
state.usedWords = [...new Set([...(state.usedWords || []), ...group.words.map(([word]) => word)])];
state.updatedAt = new Date().toISOString();

writeState(state);

console.log(`Broadcasted HANHAN word series Day ${day} for ${date}.`);
