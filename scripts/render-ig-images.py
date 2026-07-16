import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1080, 1350
MARKER = "#FFD58A"

FONT_KR = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
FONT_ZH = "/System/Library/Fonts/PingFang.ttc"
FONT_ROUND = "/System/Library/Fonts/SFNSRounded.ttf"
FONT_ROUND_BOLD = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONT_ALL = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
LINUX_CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
LINUX_CJK_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
LINUX_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LINUX_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    for candidate in [
        path,
        FONT_ZH,
        FONT_ALL,
        LINUX_CJK,
        LINUX_CJK_BOLD,
        LINUX_SANS,
        LINUX_SANS_BOLD,
    ]:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    return ImageFont.load_default()


FONTS = {
    "brand": load_font(FONT_ROUND_BOLD, 34),
    "title": load_font(FONT_ZH, 68),
    "tag": load_font(FONT_ROUND_BOLD, 19),
    "num": load_font(FONT_ROUND_BOLD, 18),
    "word": load_font(FONT_KR, 38),
    "word_sm": load_font(FONT_KR, 33),
    "meta": load_font(FONT_ALL, 22),
    "ko": load_font(FONT_KR, 20),
    "zh": load_font(FONT_ZH, 19),
    "pattern": load_font(FONT_KR, 52),
    "pattern_sm": load_font(FONT_KR, 46),
    "label": load_font(FONT_ZH, 25),
    "body": load_font(FONT_ZH, 27),
    "attach": load_font(FONT_ALL, 28),
    "ex_ko": load_font(FONT_KR, 27),
    "ex_zh": load_font(FONT_ZH, 24),
    "footer": load_font(FONT_ROUND, 24),
}

VOCAB_OVERRIDES = {
    "학교": {
        "translation": "學校",
        "exampleKo": "학교 도서관에서 친구와 같이 시험공부를 했어요.",
        "exampleZh": "我在學校圖書館和朋友一起準備考試。",
        "highlight": "학교",
    },
    "친구": {
        "translation": "朋友",
        "exampleKo": "퇴근 후에 친구를 만나서 저녁을 먹었어요.",
        "exampleZh": "下班後我和朋友見面吃了晚餐。",
        "highlight": "친구를",
    },
    "시간": {
        "translation": "時間",
        "exampleKo": "회의 시간이 바뀌어서 모두에게 다시 알려 줬어요.",
        "exampleZh": "會議時間改了，所以我重新通知了大家。",
        "highlight": "시간이",
    },
    "음식": {
        "translation": "食物，飯菜",
        "exampleKo": "점심시간에 매운 음식을 먹어서 물을 많이 마셨어요.",
        "exampleZh": "午餐時間吃了辣的食物，所以喝了很多水。",
        "highlight": "음식을",
    },
    "회의": {
        "translation": "會議",
        "exampleKo": "오전 회의에서 이번 주 업무 일정을 정했어요.",
        "exampleZh": "上午會議中決定了這週的工作時程。",
        "highlight": "회의에서",
    },
    "준비하다": {
        "translation": "準備",
        "exampleKo": "내일 발표할 자료를 오늘 미리 준비했어요.",
        "exampleZh": "我今天先準備好了明天要發表的資料。",
        "highlight": "준비했어요",
    },
    "끝나다": {
        "translation": "結束，完成",
        "exampleKo": "수업이 끝나고 친구와 카페에 갔어요.",
        "exampleZh": "下課後我和朋友去了咖啡廳。",
        "highlight": "끝나고",
    },
    "약속": {
        "translation": "約定，約會",
        "exampleKo": "오늘 저녁에는 팀장님과 식사 약속이 있어요.",
        "exampleZh": "今天晚上我和組長有飯局約定。",
        "highlight": "약속이",
    },
    "방법": {
        "translation": "方法，辦法",
        "exampleKo": "자료를 더 쉽게 정리하는 방법을 찾고 있어요.",
        "exampleZh": "我正在找更容易整理資料的方法。",
        "highlight": "방법을",
    },
    "건강": {
        "translation": "健康",
        "exampleKo": "건강을 위해 점심시간마다 조금씩 걸어요.",
        "exampleZh": "為了健康，我每天午餐時間都會稍微走路。",
        "highlight": "건강을",
    },
    "은행": {
        "translation": "銀行",
        "exampleKo": "월급이 들어와서 점심시간에 은행에 다녀왔어요.",
        "exampleZh": "薪水入帳了，所以我午休時去了銀行一趟。",
        "highlight": "은행에",
    },
    "병원": {
        "translation": "醫院",
        "exampleKo": "감기가 심해서 퇴근 후에 병원에 갔어요.",
        "exampleZh": "感冒很嚴重，所以下班後去了醫院。",
        "highlight": "병원에",
    },
    "회사원": {
        "translation": "公司職員，上班族",
        "exampleKo": "그는 서울에서 일하는 평범한 회사원이에요.",
        "exampleZh": "他是在首爾工作的普通上班族。",
        "highlight": "회사원이에요",
    },
    "직장": {
        "translation": "職場，工作單位",
        "exampleKo": "새 직장에 적응하려고 매일 메모를 많이 해요.",
        "exampleZh": "為了適應新職場，我每天都做很多筆記。",
        "highlight": "직장에",
    },
    "점심": {
        "translation": "午餐",
        "exampleKo": "오늘 점심은 동료들과 회사 근처에서 먹었어요.",
        "exampleZh": "今天午餐和同事們在公司附近吃了。",
        "highlight": "점심은",
    },
    "저녁": {
        "translation": "傍晚，晚餐",
        "exampleKo": "저녁에는 가족과 영상 통화를 할 예정이에요.",
        "exampleZh": "晚上我打算和家人視訊通話。",
        "highlight": "저녁에는",
    },
    "버스": {
        "translation": "公車",
        "exampleKo": "비가 와서 오늘은 지하철 대신 버스를 탔어요.",
        "exampleZh": "因為下雨，今天我沒搭捷運而是搭了公車。",
        "highlight": "버스를",
    },
    "날씨": {
        "translation": "天氣",
        "exampleKo": "날씨가 좋아서 점심시간에 잠깐 산책했어요.",
        "exampleZh": "天氣很好，所以午餐時間我稍微散步了一下。",
        "highlight": "날씨가",
    },
    "옷": {
        "translation": "衣服",
        "exampleKo": "내일 면접이 있어서 단정한 옷을 준비했어요.",
        "exampleZh": "明天有面試，所以我準備了端莊的衣服。",
        "highlight": "옷을",
    },
    "커피": {
        "translation": "咖啡",
        "exampleKo": "오후 회의 전에 따뜻한 커피를 한 잔 마셨어요.",
        "exampleZh": "下午會議前我喝了一杯熱咖啡。",
        "highlight": "커피를",
    },
    "가게": {
        "translation": "店，商店",
        "exampleKo": "퇴근길에 작은 가게에 들러 우유를 샀어요.",
        "exampleZh": "下班路上我順道去小店買了牛奶。",
        "highlight": "가게에",
    },
    "교실": {
        "translation": "教室",
        "exampleKo": "수업이 끝난 뒤에도 교실에 남아 단어를 외웠어요.",
        "exampleZh": "下課後我仍留在教室背單字。",
        "highlight": "교실에",
    },
    "거리": {
        "translation": "街道，路上",
        "exampleKo": "점심시간이 되자 회사 앞 거리에 사람이 많아졌어요.",
        "exampleZh": "到了午餐時間，公司前面的街道人變多了。",
        "highlight": "거리에",
    },
    "나라": {
        "translation": "國家",
        "exampleKo": "다른 나라의 문화를 배우는 일은 정말 재미있어요.",
        "exampleZh": "學習其他國家的文化真的很有趣。",
        "highlight": "나라의",
    },
    "물건": {
        "translation": "東西，物品",
        "exampleKo": "회의실에 두고 온 물건이 있어서 다시 올라갔어요.",
        "exampleZh": "因為有東西忘在會議室，我又上樓了一趟。",
        "highlight": "물건이",
    },
    "선물": {
        "translation": "禮物",
        "exampleKo": "동료의 생일이라 작은 선물을 준비했어요.",
        "exampleZh": "因為同事生日，我準備了一份小禮物。",
        "highlight": "선물을",
    },
    "질문": {
        "translation": "問題，提問",
        "exampleKo": "발표가 끝난 뒤에 질문을 세 개 받았어요.",
        "exampleZh": "發表結束後，我收到了三個提問。",
        "highlight": "질문을",
    },
    "책상": {
        "translation": "書桌，辦公桌",
        "exampleKo": "아침에 출근하자마자 책상 위를 정리했어요.",
        "exampleZh": "早上一上班，我就整理了辦公桌。",
        "highlight": "책상",
    },
    "침대": {
        "translation": "床",
        "exampleKo": "너무 피곤해서 집에 오자마자 침대에 누웠어요.",
        "exampleZh": "因為太累，我一回家就躺到床上。",
        "highlight": "침대에",
    },
    "휴일": {
        "translation": "假日，休息日",
        "exampleKo": "이번 휴일에는 집에서 밀린 드라마를 볼 거예요.",
        "exampleZh": "這個假日我要在家看之前沒追完的影集。",
        "highlight": "휴일에는",
    },
    "노래": {
        "translation": "歌，歌曲",
        "exampleKo": "출근길에 좋아하는 노래를 들으면 기분이 좋아져요.",
        "exampleZh": "上班路上聽喜歡的歌，心情會變好。",
        "highlight": "노래를",
    },
    "운전": {
        "translation": "駕駛，開車",
        "exampleKo": "비 오는 날에는 평소보다 조심해서 운전을 해요.",
        "exampleZh": "下雨天我會比平常更小心開車。",
        "highlight": "운전을",
    },
    "휴대폰": {
        "translation": "手機",
        "exampleKo": "회의 중에는 휴대폰을 무음으로 바꿔 주세요.",
        "exampleZh": "開會時請把手機改成靜音。",
        "highlight": "휴대폰을",
    },
    "뉴스": {
        "translation": "新聞",
        "exampleKo": "아침마다 뉴스를 보면서 하루 일정을 확인해요.",
        "exampleZh": "我每天早上邊看新聞邊確認一天的行程。",
        "highlight": "뉴스를",
    },
    "악화": {
        "translation": "惡化",
        "exampleKo": "부서 분위기 악화를 막기 위해 팀장님이 바로 대화를 시작했어요.",
        "exampleZh": "為了阻止部門氣氛惡化，組長立刻開始對話了。",
        "highlight": "악화를",
    },
    "큰아기": {
        "translation": "大兒媳，長媳",
        "exampleKo": "명절 준비를 도우러 큰아기가 아침 일찍 시어머니 댁에 왔어요.",
        "exampleZh": "為了幫忙準備節日，大兒媳一早就來到婆婆家了。",
        "highlight": "큰아기가",
    },
    "구도": {
        "translation": "求道，探求真理",
        "exampleKo": "그 교수는 은퇴 후에도 구도를 이어 가며 산사에서 조용히 지냈어요.",
        "exampleZh": "那位教授退休後仍持續求道，在山寺裡安靜地生活著。",
        "highlight": "구도를",
    },
    "지": {
        "translation": "從那以後",
        "exampleKo": "이사한 지 두 달이 지나서야 회사 근처 길이 익숙해졌어요.",
        "exampleZh": "搬家兩個月後，我才終於熟悉公司附近的路。",
        "highlight": "지",
    },
    "테니스": {
        "translation": "網球",
        "exampleKo": "동료와 점심시간에 테니스를 치며 스트레스를 풀었어요.",
        "exampleZh": "我和同事利用午休時間打網球，舒緩了壓力。",
        "highlight": "테니스를",
    },
    "없이": {
        "translation": "沒有，無",
        "exampleKo": "회의 준비는 별도 자료 없이 메모만 보고 진행했어요.",
        "exampleZh": "會議準備是在沒有另外資料的情況下，只看筆記進行的。",
        "highlight": "없이",
    },
    "고급화": {
        "translation": "高檔化",
        "exampleKo": "회사는 사내 식당 고급화를 위해 메뉴와 인테리어를 함께 바꿨어요.",
        "exampleZh": "公司為了讓員工餐廳高檔化，連菜單和室內裝潢都一起改了。",
        "highlight": "고급화를",
    },
    "계시되다": {
        "translation": "受啟示",
        "exampleKo": "그녀는 새벽 기도 중에 중요한 방향이 계시되었다고 말했어요.",
        "exampleZh": "她說自己在清晨祈禱時得到了重要方向的啟示。",
        "highlight": "계시되었다고",
    },
    "붕괴": {
        "translation": "崩塌，坍塌，崩潰",
        "exampleKo": "지하 작업이 길어지자 현장은 붕괴 위험 때문에 즉시 통제됐어요.",
        "exampleZh": "由於地下施工持續太久，現場因有崩塌危險而立即管制。",
        "highlight": "붕괴",
    },
    "안녕하다": {
        "translation": "平安，安寧",
        "exampleKo": "부모님은 매일 전화할 때마다 집안이 안녕한지 먼저 물으세요.",
        "exampleZh": "父母每天打電話時都會先問家裡是否平安。",
        "highlight": "안녕한지",
    },
    "그녀": {
        "exampleKo": "그녀는 회의에서 자료를 아주 차분하게 설명했어요.",
        "exampleZh": "她在會議上非常冷靜地說明了資料。",
        "highlight": "그녀는",
    },
    "매번": {
        "exampleKo": "매번 출근길이 막혀서 저는 조금 일찍 집을 나서요.",
        "exampleZh": "每次上班路上都塞車，所以我都會提早一點出門。",
        "highlight": "매번",
    },
    "연관": {
        "exampleKo": "이 질문은 이번 프로젝트 일정과 연관이 있어서 같이 검토해야 해요.",
        "exampleZh": "這個問題和這次專案時程有關，所以要一起檢討。",
        "highlight": "연관이",
    },
    "연간": {
        "exampleKo": "회사에서는 연간 교육 계획을 1월에 먼저 세워요.",
        "exampleZh": "公司會在1月先訂好年度教育計畫。",
        "highlight": "연간",
    },
    "나": {
        "exampleKo": "나는 오늘 발표 준비를 마치고 일찍 퇴근할 거예요.",
        "exampleZh": "我今天會把簡報準備好，然後提早下班。",
        "highlight": "나는",
    },
    "장갑": {
        "exampleKo": "출근길이 추워서 장갑을 꼭 챙겨 나왔어요.",
        "exampleZh": "因為上班路上很冷，所以我特地帶了手套出門。",
        "highlight": "장갑을",
    },
    "막다": {
        "exampleKo": "회의 중에는 휴대폰 알림이 집중을 막을 수 있어서 미리 꺼 두었어요.",
        "exampleZh": "會議中手機通知可能會妨礙專注，所以我事先關掉了。",
        "highlight": "막을",
    },
    "명단": {
        "exampleKo": "행사 명단에 이름이 빠지지 않았는지 다시 확인해 주세요.",
        "exampleZh": "請再確認活動名單上有沒有漏掉名字。",
        "highlight": "명단에",
    },
    "백팔십도": {
        "exampleKo": "발표 내용을 듣고 팀장의 태도가 백팔십도 달라졌어요.",
        "exampleZh": "聽完簡報內容後，組長的態度一百八十度改變了。",
        "highlight": "백팔십도",
    },
    "추모하다": {
        "exampleKo": "직원들은 먼저 세상을 떠난 동료를 함께 추모했어요.",
        "exampleZh": "員工們一起悼念了先離世的同事。",
        "highlight": "추모했어요",
    },
    "운동": {
        "exampleKo": "저는 점심시간마다 회사 근처 공원에서 운동해요.",
        "exampleZh": "我每到午休時間都會在公司附近的公園運動。",
        "highlight": "운동해요",
    },
    "한두": {
        "exampleKo": "자료를 읽어 보니 수정할 부분이 한두 군데 있었어요.",
        "exampleZh": "看過資料後，發現有一兩個地方需要修改。",
        "highlight": "한두",
    },
    "결과적": {
        "exampleKo": "결과적으로 이번 회의는 예정한 시간 안에 끝났어요.",
        "exampleZh": "結果上，這次會議在預定時間內結束了。",
        "highlight": "결과적으로",
    },
    "보급": {
        "exampleKo": "학교는 학생들에게 새 태블릿을 보급하기 시작했어요.",
        "exampleZh": "學校開始向學生配發新的平板。",
        "highlight": "보급하기",
    },
    "민주화되다": {
        "exampleKo": "회의 규칙이 민주화되면서 신입 직원도 자유롭게 의견을 냈어요.",
        "exampleZh": "隨著會議規則變得更民主化，新進員工也能自由發表意見。",
        "highlight": "민주화되면서",
    },
    "한계": {
        "translation": "限制，極限",
        "exampleKo": "이 장비로는 촬영 시간에 한계가 있어요.",
        "exampleZh": "用這台設備拍攝時間有限制。",
        "highlight": "한계가",
    },
    "떼이다": {
        "translation": "被賴帳",
        "exampleKo": "빌려준 돈을 떼일까 봐 기록을 남겼어요.",
        "exampleZh": "怕借出去的錢被賴帳，所以留下紀錄。",
        "highlight": "떼일까",
    },
    "패배하다": {
        "translation": "敗北",
        "exampleKo": "우리 팀은 마지막 경기에서 아쉽게 패배했지만 끝까지 최선을 다했어요.",
        "exampleZh": "我們隊在最後一場比賽中可惜落敗，但還是拚到了最後。",
        "highlight": "패배했지만",
    },
    "꼭": {
        "exampleKo": "내일 오전 회의에는 꼭 참석해 주세요.",
        "exampleZh": "請務必出席明天上午的會議。",
        "highlight": "꼭",
    },
    "메모하다": {
        "exampleKo": "회의 중에 나온 의견은 잊지 않도록 노트에 메모해 두었어요.",
        "exampleZh": "我把會議中提出的意見記在筆記本上，以免忘記。",
        "highlight": "메모해",
    },
    "관계하다": {
        "translation": "有關，參與",
        "exampleKo": "이 문제는 예산과 관계해서 다시 논의해야 해요.",
        "exampleZh": "這個問題和預算有關，需要再討論。",
        "highlight": "관계해서",
    },
    "돼지꿈": {
        "translation": "吉夢",
        "exampleKo": "아침에 돼지꿈을 꿔서 오늘은 왠지 일이 잘 풀릴 것 같았어요.",
        "exampleZh": "我早上夢見了豬，所以覺得今天事情好像會很順利。",
        "highlight": "돼지꿈을",
    },
    "매력적": {
        "translation": "有魅力的",
        "exampleKo": "신입 사원의 발표 방식이 차분하고 매력적이라 모두가 집중해서 들었어요.",
        "exampleZh": "新進員工的簡報方式沉穩又有魅力，大家都專心聽了。",
        "highlight": "매력적이라",
    },
    "공단": {
        "exampleKo": "우리 회사는 시내에서 조금 떨어진 공단 안에 있어요.",
        "exampleZh": "我們公司位於離市區稍遠的工業園區裡。",
        "highlight": "공단 안에",
    },
    "가격": {
        "exampleKo": "점심 가격이 올랐지만 회사 식당은 아직 부담이 적은 편이에요.",
        "exampleZh": "午餐價格雖然漲了，但公司的餐廳還算負擔不大。",
        "highlight": "가격이",
    },
    "번역어": {
        "exampleKo": "이 문장은 번역어로 옮기면 어감이 조금 달라질 수 있어요.",
        "exampleZh": "這句話如果用翻譯語來轉換，語感可能會稍微不同。",
        "highlight": "번역어로",
    },
    "광산": {
        "exampleKo": "안전 점검을 마친 뒤에야 광산 안으로 들어갈 수 있었어요.",
        "exampleZh": "完成安全檢查之後，才可以進入礦山裡面。",
        "highlight": "광산 안으로",
    },
    "넣다": {
        "exampleKo": "회의 자료는 가방에 넣어서 오후 발표 때 가져가세요.",
        "exampleZh": "請把會議資料放進包包裡，下午簡報時帶去。",
        "highlight": "넣어서",
    },
    "깎다": {
        "exampleKo": "점심 도시락을 싸려고 사과를 깎다가 손을 살짝 베었어요.",
        "exampleZh": "我為了準備午餐便當削蘋果時，不小心把手輕微劃到了。",
        "highlight": "깎다가",
    },
    "큰집": {
        "exampleKo": "명절에는 큰집에 모여서 조카들까지 다 함께 저녁을 먹어요.",
        "exampleZh": "過節時大家會聚在長房家，連姪子姪女們也一起吃晚餐。",
        "highlight": "큰집에",
    },
    "맞서다": {
        "exampleKo": "신입 직원도 부당한 요구에는 맞서서 의견을 말할 수 있어요.",
        "exampleZh": "就算是新進員工，也可以對不合理的要求表達反對意見。",
        "highlight": "맞서서",
    },
    "실거래": {
        "exampleKo": "부동산 실거래 신고는 계약이 끝난 뒤 바로 해야 해요.",
        "exampleZh": "不動產實際交易申報要在契約結束後立刻辦理。",
        "highlight": "실거래",
    },
    "구도": {
        "exampleKo": "발표 자료의 구도를 바꾸니 핵심 내용이 훨씬 잘 보였어요.",
        "exampleZh": "把簡報資料的構圖改一下後，重點內容就清楚多了。",
        "highlight": "구도를",
    },
    "높다": {
        "exampleKo": "오늘은 미세먼지 수치가 높아서 창문을 오래 열지 않았어요.",
        "exampleZh": "今天的細懸浮微粒數值很高，所以我沒有把窗戶開太久。",
        "highlight": "높아서",
    },
    "속옷": {
        "exampleKo": "여행 가기 전에 속옷을 여분으로 챙겨 가야 해요.",
        "exampleZh": "出門旅行前要多帶一套內衣褲備用。",
        "highlight": "속옷을",
    },
    "붕괴": {
        "translation": "崩塌，瓦解",
        "exampleKo": "오래된 건물은 붕괴 위험이 있어서 출입이 금지됐어요.",
        "exampleZh": "那棟老建築有倒塌危險，所以禁止進入。",
        "highlight": "붕괴",
    },
    "김": {
        "translation": "熱氣，蒸氣",
        "exampleKo": "컵라면 뚜껑을 열자 뜨거운 김이 올라왔어요.",
        "exampleZh": "打開泡麵蓋子時，熱氣冒了上來。",
        "highlight": "김이",
    },
    "약하다": {
        "translation": "弱",
        "exampleKo": "저는 커피에 약해서 오후에는 잘 마시지 않아요.",
        "exampleZh": "我對咖啡比較敏感，所以下午不太喝。",
        "highlight": "약해서",
    },
    "머리하다": {
        "translation": "做頭髮",
        "exampleKo": "면접 전에 미용실에서 머리하고 바로 회사로 갔어요.",
        "exampleZh": "面試前我去髮廊整理頭髮，然後直接去公司。",
        "highlight": "머리하고",
    },
    "뼈": {
        "translation": "骨頭",
        "exampleKo": "점심에 먹은 생선에 뼈가 많아서 천천히 먹었어요.",
        "exampleZh": "午餐吃的魚很多刺，所以我慢慢吃。",
        "highlight": "뼈가",
    },
    "독립적": {
        "translation": "獨立的",
        "exampleKo": "그 팀은 독립적으로 일정을 정하고 프로젝트를 진행해요.",
        "exampleZh": "那個團隊會獨立安排時程並推進專案。",
        "highlight": "독립적으로",
    },
    "호소": {
        "translation": "訴求，呼籲",
        "exampleKo": "고객의 호소를 듣고 담당자가 바로 상황을 확인했어요.",
        "exampleZh": "聽到顧客的訴求後，負責人立刻確認狀況。",
        "highlight": "호소를",
    },
    "얘기하다": {
        "translation": "聊天，說話",
        "exampleKo": "퇴근 후 동료와 카페에서 잠깐 얘기했어요.",
        "exampleZh": "下班後我和同事在咖啡廳聊了一下。",
        "highlight": "얘기했어요",
    },
    "여권": {
        "translation": "護照",
        "exampleKo": "출장 가기 전에 여권 만료일을 다시 확인했어요.",
        "exampleZh": "出差前我再次確認了護照效期。",
        "highlight": "여권",
    },
    "살구": {
        "translation": "杏子",
        "exampleKo": "점심 후에 동료가 나눠 준 살구를 하나 먹었어요.",
        "exampleZh": "午餐後我吃了一顆同事分的杏子。",
        "highlight": "살구를",
    },
    "위로하다": {
        "translation": "安慰",
        "exampleKo": "친구가 면접에서 떨어져서 따뜻하게 위로했어요.",
        "exampleZh": "朋友面試沒上，所以我溫柔地安慰了他。",
        "highlight": "위로했어요",
    },
    "정권": {
        "translation": "政權",
        "exampleKo": "뉴스에서는 새 정권의 경제 정책을 자세히 다뤘어요.",
        "exampleZh": "新聞詳細報導了新政權的經濟政策。",
        "highlight": "정권의",
    },
    "항복": {
        "translation": "投降",
        "exampleKo": "게임에서 계속 지자 친구가 결국 항복을 선언했어요.",
        "exampleZh": "朋友在遊戲裡一直輸，最後宣布投降。",
        "highlight": "항복을",
    },
    "책": {
        "translation": "書",
        "exampleKo": "출근길에 읽으려고 가방에 책을 한 권 넣었어요.",
        "exampleZh": "我放了一本書在包包裡，打算通勤時讀。",
        "highlight": "책을",
    },
    "공개": {
        "translation": "公開",
        "exampleKo": "새 제품 정보는 다음 주 회의에서 공개될 예정이에요.",
        "exampleZh": "新產品資訊預計在下週會議公開。",
        "highlight": "공개될",
    },
    "보급하다": {
        "translation": "普及，供應",
        "exampleKo": "회사는 새 업무 도구를 전 직원에게 보급하고 있어요.",
        "exampleZh": "公司正在把新的工作工具提供給全體員工使用。",
        "highlight": "보급하고",
    },
    "논란": {
        "translation": "爭議",
        "exampleKo": "그 결정은 직원들 사이에서 큰 논란이 되었어요.",
        "exampleZh": "那個決定在員工之間引起了很大的爭議。",
        "highlight": "논란이",
    },
    "통로": {
        "translation": "通道",
        "exampleKo": "비상 통로 앞에는 물건을 두면 안 돼요.",
        "exampleZh": "緊急通道前不能放東西。",
        "highlight": "통로",
    },
    "회사": {
        "translation": "公司",
        "exampleKo": "우리 회사는 금요일마다 조금 일찍 퇴근해요.",
        "exampleZh": "我們公司每週五都會稍微早點下班。",
        "highlight": "회사",
    },
    "다녀오다": {
        "translation": "去一趟回來",
        "exampleKo": "점심시간에 은행에 잠깐 다녀왔어요.",
        "exampleZh": "午休時間我去了一下銀行回來。",
        "highlight": "다녀왔어요",
    },
    "검토하다": {
        "translation": "檢討，審查",
        "exampleKo": "팀장은 보고서를 검토한 뒤에 의견을 보내 줬어요.",
        "exampleZh": "組長審查報告後，把意見寄給我了。",
        "highlight": "검토한",
    },
    "무가치하다": {
        "translation": "沒有價值",
        "exampleKo": "작은 기록도 나중에는 무가치하지 않을 수 있어요.",
        "exampleZh": "小小的紀錄之後也可能不是毫無價值。",
        "highlight": "무가치하지",
    },
    "침해": {
        "translation": "侵害",
        "exampleKo": "개인 정보 침해를 막기 위해 비밀번호를 자주 바꿔요.",
        "exampleZh": "為了防止個資侵害，我常更換密碼。",
        "highlight": "침해를",
    },
    "역시": {
        "translation": "果然，也",
        "exampleKo": "오래 준비한 발표라서 역시 반응이 좋았어요.",
        "exampleZh": "因為準備很久，發表反應果然很好。",
        "highlight": "역시",
    },
    "화요일": {
        "translation": "星期二",
        "exampleKo": "다음 화요일에는 오전 회의가 없어서 조금 여유로워요.",
        "exampleZh": "下週二早上沒有會議，所以比較從容。",
        "highlight": "화요일에는",
    },
    "그녀": {
        "translation": "她",
        "exampleKo": "그녀는 새 프로젝트를 맡고 매일 늦게까지 일했어요.",
        "exampleZh": "她接下新專案後，每天都工作到很晚。",
        "highlight": "그녀는",
    },
    "계시되다": {
        "translation": "被啟示",
        "exampleKo": "그 내용은 오래된 기록에 계시된 이야기로 소개됐어요.",
        "exampleZh": "那個內容被介紹為古老記錄中所啟示的故事。",
        "highlight": "계시된",
    },
    "입법": {
        "translation": "立法",
        "exampleKo": "새로운 입법 논의가 다음 달부터 본격적으로 시작돼요.",
        "exampleZh": "新的立法討論將從下個月正式開始。",
        "highlight": "입법",
    },
    "넘다": {
        "exampleKo": "회의 시간이 한 시간을 넘어서 모두가 잠깐 쉬어 갔어요.",
        "exampleZh": "會議時間超過了一小時，所以大家稍微休息了一下。",
        "highlight": "넘어서",
    },
    "그러므로": {
        "exampleKo": "보고서에 근거가 부족했어요. 그러므로 다시 확인해야 해요.",
        "exampleZh": "報告書的依據不夠，所以必須重新確認。",
        "highlight": "그러므로",
    },
    "뜻하다": {
        "exampleKo": "이 표시는 출입 금지를 뜻해서 문 앞에 붙여 두었어요.",
        "exampleZh": "這個標示表示禁止進入，所以我把它貼在門口了。",
        "highlight": "뜻해서",
    },
    "위로되다": {
        "exampleKo": "동료의 짧은 응원 한마디가 생각보다 크게 위로되었어요.",
        "exampleZh": "同事一句簡短的加油，出乎意料地給了我很大的安慰。",
        "highlight": "위로되었어요",
    },
    "오래달리기": {
        "exampleKo": "체육 시간에는 오래달리기를 해서 마지막까지 속도를 유지했어요.",
        "exampleZh": "體育課時我們跑了長跑，並且把速度維持到最後。",
        "highlight": "오래달리기를",
    },
    "믿다": {
        "translation": "相信",
        "exampleKo": "팀원들은 서로를 믿고 어려운 일정을 함께 버텼어요.",
        "exampleZh": "團隊成員互相信任，一起撐過困難的時程。",
        "highlight": "믿고",
    },
    "외국어": {
        "translation": "外語",
        "exampleKo": "외국어를 잘하면 해외 고객과 일할 때 도움이 돼요.",
        "exampleZh": "外語好，在和海外客戶合作時會有幫助。",
        "highlight": "외국어를",
    },
    "관계없다": {
        "translation": "沒有關係",
        "exampleKo": "이 문제는 제 담당 업무와 관계없지만 확인해 볼게요.",
        "exampleZh": "這個問題和我的負責業務無關，但我會確認看看。",
        "highlight": "관계없지만",
    },
    "매번": {
        "translation": "每次",
        "exampleKo": "그는 매번 회의 전에 자료를 꼼꼼히 확인해요.",
        "exampleZh": "他每次開會前都會仔細確認資料。",
        "highlight": "매번",
    },
    "입문": {
        "translation": "入門",
        "exampleKo": "한국어 입문 수업은 발음부터 천천히 배워요.",
        "exampleZh": "韓文入門課會從發音開始慢慢學。",
        "highlight": "입문",
    },
    "삼": {
        "translation": "三",
        "exampleKo": "회의 자료는 총 삼 부를 출력해서 가져가세요.",
        "exampleZh": "請把會議資料總共印三份帶來。",
        "highlight": "삼",
    },
    "평일": {
        "translation": "平日",
        "exampleKo": "평일 아침에는 지하철이 항상 많이 붐벼요.",
        "exampleZh": "平日早上的地鐵總是很擁擠。",
        "highlight": "평일",
    },
    "듣기": {
        "translation": "聽力",
        "exampleKo": "TOPIK 듣기 연습은 출근길에 짧게 해도 도움이 돼요.",
        "exampleZh": "TOPIK 聽力練習即使在通勤時短短做一下也有幫助。",
        "highlight": "듣기",
    },
    "보급되다": {
        "translation": "被普及",
        "exampleKo": "새 결제 시스템이 매장에 빠르게 보급되고 있어요.",
        "exampleZh": "新的付款系統正在店面快速普及。",
        "highlight": "보급되고",
    },
    "이": {
        "exampleKo": "이 보고서는 오늘 회의에서 팀장님께 제출할 예정이에요.",
        "exampleZh": "這份報告預計今天在會議上交給組長。",
        "highlight": "이",
    },
    "다": {
        "exampleKo": "서류는 다 정리했으니 이제 가방에 넣으면 돼요.",
        "exampleZh": "文件都整理好了，所以現在放進包包裡就可以了。",
        "highlight": "다",
    },
    "하다": {
        "exampleKo": "학생들은 조별 과제를 하다 보니 서로 더 친해졌어요.",
        "exampleZh": "學生們一邊做小組作業，一邊變得更加熟悉了。",
        "highlight": "하다",
    },
    "한": {
        "exampleKo": "한 시간만 더 일하면 오늘 업무는 끝나요.",
        "exampleZh": "只要再工作一個小時，今天的工作就結束了。",
        "highlight": "한 시간만",
    },
    "도": {
        "exampleKo": "회의가 길어져도 저는 끝까지 자리를 지켰어요.",
        "exampleZh": "即使會議拖長了，我也一直待到最後。",
        "highlight": "도",
    },
    "있다": {
        "exampleKo": "지금 도서관에 있어서 잠깐 후에 전화드릴게요.",
        "exampleZh": "我現在在圖書館，所以過一會兒再打給您。",
        "highlight": "있어서",
    },
    "어": {
        "exampleKo": "어, 회의 시간이 벌써 바뀌었네요.",
        "exampleZh": "咦，會議時間已經改了呢。",
        "highlight": "어,",
    },
    "일": {
        "exampleKo": "오늘 일은 퇴근 전에 마무리하고 가야 해요.",
        "exampleZh": "今天的工作得在下班前完成再走。",
        "highlight": "일은",
    },
    "나": {
        "exampleKo": "나도 팀 회의 전에 자료를 한번 더 확인할게.",
        "exampleZh": "我也會在團隊會議前再確認一次資料。",
        "highlight": "나도",
    },
    "지": {
        "exampleKo": "입사한 지 석 달이 지나서 이제 업무 흐름이 익숙해졌어요.",
        "exampleZh": "自從入職三個月後，現在已經熟悉工作流程了。",
        "highlight": "지",
    },
    "주거하다": {
        "exampleKo": "서울에 주거하는 학생들은 통학 시간이 짧아서 편하다고 했어요.",
        "exampleZh": "住在首爾的學生們說，因為通學時間短所以很方便。",
        "highlight": "주거하는",
    },
    "무": {
        "exampleKo": "엄마는 저녁 국에 무를 넣어서 시원한 맛을 냈어요.",
        "exampleZh": "媽媽在晚餐湯裡放了白蘿蔔，做出了清爽的味道。",
        "highlight": "무를",
    },
    "글쎄요": {
        "exampleKo": "글쎄요, 이번 회의 안건은 팀장님이 먼저 정하실 것 같아요.",
        "exampleZh": "這個嘛，我想這次會議議程應該會由組長先決定。",
        "highlight": "글쎄요",
    },
    "확인되다": {
        "exampleKo": "지각 사유가 사실로 확인되자 선생님이 출석부를 다시 살폈어요.",
        "exampleZh": "遲到原因被確認屬實後，老師又看了一次點名簿。",
        "highlight": "확인되자",
    },
    "팁": {
        "exampleKo": "선배가 발표 자료를 만들 때는 핵심 문장을 먼저 적으라고 팁을 줬어요.",
        "exampleZh": "前輩給了我建議，說做簡報資料時要先寫下重點句。",
        "highlight": "팁을",
    },
    "계시하다": {
        "exampleKo": "교수님은 연구 방향을 설명하며 관련 문헌을 하나씩 계시해 주셨어요.",
        "exampleZh": "教授說明研究方向時，還一一提示了相關文獻。",
        "highlight": "계시해",
    },
    "처형되다": {
        "exampleKo": "오래된 법에 따라 죄인이 공개적으로 처형되었다는 기록이 남아 있어요.",
        "exampleZh": "有記錄顯示，依照舊法，罪犯曾被公開處刑。",
        "highlight": "처형되었다는",
    },
    "얘기": {
        "exampleKo": "점심시간에 동료와 퇴근 후 얘기를 잠깐 나눴어요.",
        "exampleZh": "午餐時間我和同事簡單聊了一下下班後的事情。",
        "highlight": "얘기를",
    },
    "갚다": {
        "exampleKo": "이번 달 월급을 받으면 친구에게 빌린 돈을 바로 갚을 거예요.",
        "exampleZh": "這個月領到薪水後，我會立刻還朋友借給我的錢。",
        "highlight": "갚을",
    },
    "막": {
        "exampleKo": "회의가 막 시작했으니 지금 들어가도 괜찮아요.",
        "exampleZh": "會議才剛開始，所以現在進去也沒關係。",
        "highlight": "막 시작했으니",
    },
    "접근법": {
        "exampleKo": "팀장은 문제를 해결하는 접근법을 다시 설명해 주었다.",
        "exampleZh": "組長又說明了一次解決問題的方法。",
        "highlight": "접근법을",
    },
    "저리되다": {
        "exampleKo": "프로젝트가 계속 미뤄지면 일이 저리될 수 있어요.",
        "exampleZh": "如果專案一直延後，事情可能會變成那樣。",
        "highlight": "저리될",
    },
    "괜찮다": {
        "exampleKo": "오늘 회의 일정은 오후라서 저는 괜찮아요.",
        "exampleZh": "今天的會議時間在下午，所以我沒問題。",
        "highlight": "괜찮아요",
    },
    "셋째": {
        "exampleKo": "이번 보고서에서는 셋째 항목을 먼저 검토합시다.",
        "exampleZh": "這份報告裡，我們先檢查第三項吧。",
        "highlight": "셋째",
    },
    "첫사랑": {
        "exampleKo": "동창회에서 민준은 첫사랑 이야기를 조심스럽게 꺼냈다.",
        "exampleZh": "在同學會上，民俊小心翼翼地提起了初戀的話題。",
        "highlight": "첫사랑",
    },
    "실망시키다": {
        "exampleKo": "약속을 지키지 못한 직원은 팀원들을 실망시켰다.",
        "exampleZh": "那位沒能遵守約定的員工讓團隊成員失望了。",
        "highlight": "실망시켰다",
    },
    "회원제": {
        "exampleKo": "이 헬스장은 회원제로 운영돼서 등록이 필요해요.",
        "exampleZh": "這間健身房採會員制營運，所以需要登記。",
        "highlight": "회원제로",
    },
    "저리하다": {
        "exampleKo": "선배는 후배가 실수해도 저리하지 않고 차분하게 알려 주었다.",
        "exampleZh": "學長就算學弟犯錯也沒有那樣做，而是冷靜地告訴了他。",
        "highlight": "저리하지",
    },
    "드리다": {
        "exampleKo": "상무님께 자료를 드리기 전에 다시 확인했습니다.",
        "exampleZh": "在把資料交給常務之前，我又確認了一次。",
        "highlight": "드리기",
    },
    "시골": {
        "exampleKo": "주말이면 저는 시골에 내려가 할머니를 도와드려요.",
        "exampleZh": "到了週末，我會去鄉下幫奶奶。",
        "highlight": "시골에",
    },
    "손님": {
        "exampleKo": "오늘 카페에 손님이 많아요.",
        "exampleZh": "今天咖啡廳客人很多。",
        "highlight": "손님",
    },
    "없이": {
        "exampleKo": "저는 설탕 없이 커피를 마셔요.",
        "exampleZh": "我喝咖啡不加糖。",
        "highlight": "없이",
    },
    "악화": {
        "exampleKo": "감기가 악화돼서 병원에 갔어요.",
        "exampleZh": "感冒變嚴重，所以我去了醫院。",
        "highlight": "악화",
    },
    "가끔가다가": {
        "exampleKo": "가끔가다가 혼자 영화를 봐요.",
        "exampleZh": "我偶爾會一個人看電影。",
        "highlight": "가끔가다가",
    },
    "저리다": {
        "exampleKo": "오래 앉아 있었더니 다리가 저려요.",
        "exampleZh": "坐太久了，腿有點麻。",
        "highlight": "저려요",
    },
    "안녕하다": {
        "exampleKo": "오랜만이에요. 그동안 안녕하셨어요?",
        "exampleZh": "好久不見，這段時間你過得好嗎？",
        "highlight": "안녕하셨어요",
    },
    "택배": {
        "exampleKo": "오늘 택배가 집에 도착했어요.",
        "exampleZh": "今天包裹送到家了。",
        "highlight": "택배",
    },
    "첫차": {
        "exampleKo": "내일은 첫차를 타고 공항에 가야 해요.",
        "exampleZh": "明天要搭首班車去機場。",
        "highlight": "첫차",
    },
    "고급화": {
        "exampleKo": "이 브랜드는 제품 고급화에 힘쓰고 있어요.",
        "exampleZh": "這個品牌正在努力讓產品更高級化。",
        "highlight": "고급화",
    },
    "민주화하다": {
        "exampleKo": "사람들은 사회를 더 민주화하려고 노력했어요.",
        "exampleZh": "人們努力讓社會更加民主化。",
        "highlight": "민주화하려고",
    },
    "나라님": {
        "exampleKo": "옛날 이야기에서 백성들은 나라님을 존경했어요.",
        "exampleZh": "在古老故事裡，百姓們尊敬國君。",
        "highlight": "나라님",
    },
    "긍정적": {
        "exampleKo": "팀장님은 제 제안에 긍정적인 반응을 보였어요.",
        "exampleZh": "主管對我的提案表現出正面的反應。",
        "highlight": "긍정적인",
    },
    "계시": {
        "exampleKo": "그는 힘든 시기에 계시를 받은 것처럼 마음이 편해졌어요.",
        "exampleZh": "他在困難時期像得到啟示一樣，心情變得平靜。",
        "highlight": "계시",
    },
    "치명적": {
        "exampleKo": "작은 실수가 프로젝트에 치명적인 문제가 될 수 있어요.",
        "exampleZh": "小小的失誤也可能成為專案中的致命問題。",
        "highlight": "치명적인",
    },
    "의미하다": {
        "exampleKo": "이 표시는 회의실을 사용할 수 없다는 뜻을 의미해요.",
        "exampleZh": "這個標示表示會議室不能使用。",
        "highlight": "의미해요",
    },
    "낚시하다": {
        "exampleKo": "주말에 아버지와 강에서 낚시했어요.",
        "exampleZh": "週末我和爸爸在河邊釣魚。",
        "highlight": "낚시했어요",
    },
    "별생각": {
        "exampleKo": "처음에는 별생각 없이 회의에 들어갔어요.",
        "exampleZh": "一開始我沒想太多就進了會議。",
        "highlight": "별생각",
    },
    "돼지머리": {
        "exampleKo": "개업식 때 상 위에 돼지머리를 올려 두었어요.",
        "exampleZh": "開幕儀式時，桌上放了豬頭。",
        "highlight": "돼지머리",
    },
    "값있다": {
        "exampleKo": "실패한 경험도 나중에는 값있는 배움이 되었어요.",
        "exampleZh": "失敗的經驗後來也成了寶貴的學習。",
        "highlight": "값있는",
    },
    "눌러앉다": {
        "exampleKo": "친구 집에 잠깐 갔다가 저녁까지 눌러앉았어요.",
        "exampleZh": "我只是去朋友家一下，結果一直待到晚上。",
        "highlight": "눌러앉았어요",
    },
    "악화되다": {
        "exampleKo": "회사의 상황이 더 악화되지 않았어요.",
        "exampleZh": "公司的情況沒有再惡化。",
        "highlight": "악화되지",
    },
    "값하다": {
        "exampleKo": "이 노트북은 비싸지만 성능이 좋아서 값해요.",
        "exampleZh": "這台筆電雖然貴，但很值得。",
        "highlight": "값해요",
    },
    "압도되다": {
        "exampleKo": "큰 무대에 압도되어 말을 못 했어요.",
        "exampleZh": "我被大場面震懾住，說不出話。",
        "highlight": "압도되어",
    },
    "하루": {
        "exampleKo": "오늘 하루도 정말 바쁘게 지나갔어요.",
        "exampleZh": "今天一整天也過得非常忙碌。",
        "highlight": "하루",
    },
    "글쎄": {
        "exampleKo": "글쎄, 이번 주 안에 끝낼 수 있을지 모르겠어요.",
        "exampleZh": "這個嘛，我不確定這週內能不能完成。",
        "highlight": "글쎄",
    },
    "인간적": {
        "pos": "형용사",
        "translation": "有人情味的",
        "exampleKo": "그는 인간적으로 제 상황을 이해해 줬어요.",
        "exampleZh": "他很有人情味地體諒了我的情況。",
        "highlight": "인간적으로",
    },
    "악화하다": {
        "exampleKo": "무리한 야근은 건강을 악화할 수 있어요.",
        "exampleZh": "過度加班可能會使健康惡化。",
        "highlight": "악화할",
    },
    "꽃답다": {
        "exampleKo": "졸업식 날 학생들의 웃음이 꽃답게 빛났어요.",
        "exampleZh": "畢業典禮那天，學生們笑得燦爛。",
        "highlight": "꽃답게",
    },
    "압도하다": {
        "exampleKo": "그 선수는 뛰어난 실력으로 상대를 압도했어요.",
        "exampleZh": "那位選手以出色實力壓倒了對手。",
        "highlight": "압도했어요",
    },
    "언제": {
        "exampleKo": "회의가 언제 시작하는지 다시 확인해 주세요.",
        "exampleZh": "請再確認會議什麼時候開始。",
        "highlight": "언제",
    },
    "장갑": {
        "exampleKo": "출근길이 추워서 장갑을 꼭 챙겨 나왔어요.",
        "exampleZh": "因為上班路上很冷，所以我一定帶了手套出門。",
        "highlight": "장갑을",
    },
    "막다": {
        "exampleKo": "회의실 문이 바람에 열리지 않도록 책상으로 막았어요.",
        "exampleZh": "我用桌子把會議室的門擋住，避免被風吹開。",
        "highlight": "막았어요",
    },
    "명단": {
        "exampleKo": "인사팀이 오후 회의 참석자 명단을 다시 확인했어요.",
        "exampleZh": "人事部又確認了一次下午會議出席者名單。",
        "highlight": "명단을",
    },
    "백팔십도": {
        "exampleKo": "프로젝트 방향이 바뀌면서 일정도 백팔십도로 달라졌어요.",
        "exampleZh": "因為專案方向改變，時程也完全變了。",
        "highlight": "백팔십도로",
    },
    "추모하다": {
        "translation": "追思，悼念",
        "exampleKo": "학생들은 선생님을 함께 추모했어요.",
        "exampleZh": "學生們一起悼念了老師。",
        "highlight": "추모했어요",
    },
    "운동": {
        "exampleKo": "저는 퇴근 후에 동네 공원에서 운동을 해요.",
        "exampleZh": "我下班後會在住家附近的公園運動。",
        "highlight": "운동을",
    },
    "한두": {
        "exampleKo": "보고서를 제출하기 전에 한두 군데만 더 확인해 주세요.",
        "exampleZh": "在交報告之前，請再確認一兩個地方就好。",
        "highlight": "한두",
    },
    "결과적": {
        "exampleKo": "결과적으로 이번 발표는 팀에 좋은 기회가 되었어요.",
        "exampleZh": "最終，這次發表成了團隊的一個好機會。",
        "highlight": "결과적으로",
    },
    "보급": {
        "exampleKo": "회사에서는 새로운 보안 프로그램 보급을 서두르고 있어요.",
        "exampleZh": "公司正在加緊推廣新的資安程式。",
        "highlight": "보급을",
    },
    "민주화되다": {
        "exampleKo": "요즘은 회의 방식이 더 민주화되어서 누구나 의견을 내기 쉬워요.",
        "exampleZh": "最近會議方式變得更民主化，所以任何人都更容易提出意見。",
        "highlight": "민주화되어",
    },
    "새사람": {
        "translation": "像變了個人",
        "exampleKo": "입사 후 그는 새사람처럼 성실해졌어요.",
        "exampleZh": "入職後，他像變了個人一樣變得認真。",
        "highlight": "새사람처럼",
    },
    "에이": {
        "exampleKo": "에이, 실수는 누구나 할 수 있으니 너무 걱정하지 마세요.",
        "exampleZh": "唉，誰都可能會犯錯，所以不要太擔心。",
        "highlight": "에이,",
    },
    "죽어지내다": {
        "translation": "低調過日子",
        "exampleKo": "취업 준비가 길어져서 요즘은 방에서 거의 죽어지내고 있어요.",
        "exampleZh": "因為求職準備拖得很久，我最近幾乎都窩在房間裡過日子。",
        "highlight": "죽어지내고",
    },
    "타격하다": {
        "translation": "打擊，攻擊",
        "exampleKo": "상대 팀의 약점을 타격했어요.",
        "exampleZh": "攻擊了對方隊伍的弱點。",
        "highlight": "타격했어요",
    },
    "여러분": {
        "translation": "各位",
        "exampleKo": "여러분, 지금부터 오늘 발표를 시작하겠습니다.",
        "exampleZh": "各位，現在開始今天的發表。",
        "highlight": "여러분,",
    },
    "검정색": {
        "exampleKo": "회의 때는 검정색 정장을 입어야 해서 미리 준비했어요.",
        "exampleZh": "開會時必須穿黑色西裝，所以我先準備好了。",
        "highlight": "검정색",
    },
    "관계있다": {
        "translation": "有關",
        "exampleKo": "이 자료는 이번 프로젝트와 관계가 있어요.",
        "exampleZh": "這份資料和這次專案有關。",
        "highlight": "관계가",
    },
    "위로": {
        "translation": "安慰",
        "exampleKo": "친구가 힘들어 보여서 따뜻한 위로를 건넸어요.",
        "exampleZh": "朋友看起來很辛苦，所以我送上了溫暖的慰勞。",
        "highlight": "위로를",
    },
    "하늘거리다": {
        "exampleKo": "창가 커튼이 바람에 하늘거리며 오후 햇빛을 받았어요.",
        "exampleZh": "窗邊的窗簾隨風飄搖，映著午後的陽光。",
        "highlight": "하늘거리며",
    },
    "특유하다": {
        "translation": "獨特",
        "exampleKo": "그 카페는 특유한 분위기로 유명해요.",
        "exampleZh": "那間咖啡廳以獨特的氛圍聞名。",
        "highlight": "특유한",
    },
    "신규": {
        "translation": "新進的，新的",
        "exampleKo": "이번 달부터 신규 직원 교육이 시작돼요.",
        "exampleZh": "從這個月開始，新進員工的教育訓練要開始了。",
        "highlight": "신규 직원",
    },
    "염려": {
        "translation": "擔心，憂慮",
        "exampleKo": "비가 올까 봐 행사 일정이 조금 염려돼요.",
        "exampleZh": "因為怕下雨，所以有點擔心活動日程。",
        "highlight": "염려돼요",
    },
    "연결": {
        "translation": "連接，連結",
        "exampleKo": "회의실 와이파이에 노트북을 연결해 주세요.",
        "exampleZh": "請把筆電連接到會議室的 Wi-Fi。",
        "highlight": "연결해",
    },
    "연극": {
        "translation": "話劇，戲劇",
        "exampleKo": "주말에 학생들과 연극 공연을 보러 갔어요.",
        "exampleZh": "週末我和學生們去看了話劇演出。",
        "highlight": "연극 공연",
    },
    "연관": {
        "translation": "相關，關聯",
        "exampleKo": "이 자료는 이번 프로젝트와 연관이 있어요.",
        "exampleZh": "這份資料和這次專案有關聯。",
        "highlight": "연관이",
    },
    "연간": {
        "translation": "年度的，全年",
        "exampleKo": "회사는 연간 매출 보고서를 이번 주에 제출했어요.",
        "exampleZh": "公司這週提交了年度營收報告。",
        "highlight": "연간 매출",
    },
    "도달하다": {
        "translation": "到達，達到",
        "exampleKo": "택배가 오후 세 시쯤 학교에 도달했어요.",
        "exampleZh": "包裹大約在下午三點送達學校。",
        "highlight": "도달했어요",
    },
    "애초": {
        "translation": "起初，一開始",
        "exampleKo": "애초에 일정이 너무 빡빡해서 회의가 길어졌어요.",
        "exampleZh": "一開始行程就太緊湊，所以會議拖長了。",
        "highlight": "애초에",
    },
    "답": {
        "translation": "答案，回答",
        "exampleKo": "선생님은 학생의 답을 듣고 다시 설명해 주셨어요.",
        "exampleZh": "老師聽了學生的回答後，又重新說明了一次。",
        "highlight": "답을",
    },
    "연락처": {
        "translation": "聯絡方式，聯絡電話",
        "exampleKo": "행사 변경 사항은 연락처로 바로 보내 드릴게요.",
        "exampleZh": "活動變更事項我會直接傳到聯絡方式上。",
        "highlight": "연락처로",
    },
    "붕괴": {
        "translation": "崩塌，崩潰",
        "exampleKo": "오래된 건물은 붕괴 위험이 있어서 출입이 금지됐어요.",
        "exampleZh": "那棟老舊建築有倒塌風險，所以禁止進入。",
        "highlight": "붕괴 위험",
    },
    "얘기하다": {
        "translation": "說話，談論",
        "exampleKo": "점심시간에 팀장님과 다음 주 일정에 대해 얘기했어요.",
        "exampleZh": "午休時間我和組長談了下週的行程。",
        "highlight": "얘기했어요",
    },
    "테니스": {
        "translation": "網球",
        "exampleKo": "저는 퇴근 후에 동호회 사람들과 테니스를 쳐요.",
        "exampleZh": "我下班後會和社團的人一起打網球。",
        "highlight": "테니스를",
    },
    "관련되다": {
        "translation": "有關，相關",
        "exampleKo": "이 질문은 지난 회의에서 나온 안건과 관련돼 있어요.",
        "exampleZh": "這個問題和上次會議提出的議題有關。",
        "highlight": "관련돼",
    },
    "검토되다": {
        "translation": "被檢討，被審查",
        "exampleKo": "제안서는 오늘 오후 회의에서 다시 검토될 예정이에요.",
        "exampleZh": "提案書預計在今天下午的會議上再次被檢討。",
        "highlight": "검토될",
    },
    "큰아기": {
        "translation": "大兒媳，長媳",
        "exampleKo": "명절 준비를 도우러 큰아기가 아침 일찍 시어머니 댁에 왔어요.",
        "exampleZh": "為了幫忙準備節日，大兒媳一早就來到婆婆家了。",
        "highlight": "큰아기가",
    },
    "업소": {
        "translation": "店家，營業場所",
        "exampleKo": "이 업소는 점심시간에 손님이 많이 몰려요.",
        "exampleZh": "這家店在午餐時間會湧入很多客人。",
        "highlight": "업소는",
    },
    "운동하다": {
        "translation": "運動，鍛鍊",
        "exampleKo": "저는 아침마다 집 근처 공원에서 운동해요.",
        "exampleZh": "我每天早上都會在住家附近的公園運動。",
        "highlight": "운동해요",
    },
    "삼촌": {
        "translation": "叔叔，舅舅",
        "exampleKo": "삼촌이 주말에 사과를 한 상자 사 오셨어요.",
        "exampleZh": "叔叔週末買來了一整箱蘋果。",
        "highlight": "삼촌이",
    },
    "질": {
        "translation": "品質，質量",
        "exampleKo": "이 원단은 가격은 조금 비싸도 질이 좋아요.",
        "exampleZh": "這種布料雖然價格高一點，但品質很好。",
        "highlight": "질이",
    },
}


def display_vocab_row(row):
    override = VOCAB_OVERRIDES.get(row.get("word"))
    if override:
        item = {**row, **override}
        return normalize_vocab_item(item)
    word = row.get("word", "未知單字")
    raise ValueError(f"Missing curated vocabulary example for {word}. Add it to VOCAB_OVERRIDES before rendering.")


def adjective_translation(text):
    parts = [part.strip() for part in text.split("，")]
    normalized = []
    for part in parts:
        if not part:
            continue
        normalized.append(part if part.endswith("的") else f"{part}的")
    return "，".join(normalized)


def normalize_vocab_item(item):
    normalized = dict(item)
    if normalized.get("pos") == "형용사" and normalized.get("translation"):
        normalized["translation"] = adjective_translation(normalized["translation"])
    return normalized


def argos_translator():
    try:
        from argostranslate import translate

        languages = {lang.code: lang for lang in translate.load_installed_languages()}
        ko = languages.get("ko")
        zh = languages.get("zh")
        en = languages.get("en")
        if ko and zh:
            direct = ko.get_translation(zh)
            if direct:
                return lambda text: direct.translate(text)
        if ko and en and zh:
            ko_en = ko.get_translation(en)
            en_zh = en.get_translation(zh)
            if ko_en and en_zh:
                return lambda text: en_zh.translate(ko_en.translate(text))
    except Exception:
        return None
    return None


TRANSLATE = argos_translator()


def translate_example(row):
    if row.get("exampleZh"):
        return row["exampleZh"]
    return f"詞義：{row.get('translation') or row.get('definitionZh') or '整理中'}"


def text_example_or_definition(row):
    if row.get("exampleZh"):
        return row["exampleZh"]
    translated = translate_example(row)
    if translated and translated != "例句翻譯整理中":
        return translated
    if row.get("definitionZh"):
        return f"詞義：{row['definitionZh']}"
    return "例句翻譯整理中"


def gradient(bg1=(255, 248, 244), bg2=(238, 247, 241)):
    img = Image.new("RGB", (WIDTH, HEIGHT), bg1)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = tuple(int(bg1[i] * (1 - t) + bg2[i] * t) for i in range(3))
        draw.line([(0, y), (WIDTH, y)], fill=color)
    return img, draw


def ellipsize(draw, text, font, max_width):
    if draw.textlength(text, font=font) <= max_width:
        return text
    clipped = text
    while clipped and draw.textlength(f"{clipped}...", font=font) > max_width:
        clipped = clipped[:-1]
    return f"{clipped}..."


def fit_font(draw, text, font, max_width, min_size=15):
    current = font
    while draw.textlength(text, font=current) > max_width and getattr(current, "size", min_size) > min_size:
        current = current.font_variant(size=current.size - 1)
    return current


def draw_fit_line(draw, x, y, text, font, fill, max_width, min_size=15):
    fitted = fit_font(draw, text, font, max_width, min_size)
    if draw.textlength(text, font=fitted) > max_width:
        text = ellipsize(draw, text, fitted, max_width)
    draw.text((x, y), text, font=fitted, fill=fill)
    bbox = draw.textbbox((x, y), text, font=fitted)
    return y + (bbox[3] - bbox[1])


def draw_fit_or_wrap(draw, x, y, text, font, fill, max_width, max_lines=2, min_size=18, gap=4):
    fitted = fit_font(draw, text, font, max_width, min_size)
    if draw.textlength(text, font=fitted) <= max_width:
        draw.text((x, y), text, font=fitted, fill=fill)
        bbox = draw.textbbox((x, y), text, font=fitted)
        return y + (bbox[3] - bbox[1])

    lines = []
    line = ""
    for char in text:
        test = line + char
        if draw.textlength(test, font=fitted) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = char
            if len(lines) >= max_lines - 1:
                break
    remaining = text[len("".join(lines)):]
    if remaining:
        line = ""
        for char in remaining:
            test = line + char
            if draw.textlength(test, font=fitted) <= max_width:
                line = test
            else:
                break
        if line:
            lines.append(line)

    for line in lines[:max_lines]:
        draw.text((x, y), line, font=fitted, fill=fill)
        bbox = draw.textbbox((x, y), line, font=fitted)
        y += (bbox[3] - bbox[1]) + gap
    return y - gap


def wrap(draw, text, xy, font, fill, max_width, max_lines=2, gap=4):
    x, y = xy
    lines = []
    line = ""
    for char in text:
        test = line + char
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = char
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = ellipsize(draw, lines[-1], font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + gap
    return y


def draw_marker(draw, x, y, text, target, max_width, font, fill):
    shown = text
    font = fit_font(draw, shown, font, max_width, 15)
    if not target or target not in shown:
        draw.text((x, y), shown, font=font, fill=fill)
        return y + 25

    pre, rest = shown.split(target, 1)
    tx = x
    draw.text((tx, y), pre, font=font, fill=fill)
    tx += draw.textlength(pre, font=font)
    target_width = draw.textlength(target, font=font)
    draw.rounded_rectangle([tx - 2, y + 13, tx + target_width + 3, y + 25], radius=5, fill=MARKER)
    draw.text((tx, y), target, font=font, fill=fill)
    tx += target_width
    draw.text((tx, y), rest, font=font, fill=fill)
    return y + 25


def draw_header(draw, title):
    draw.rounded_rectangle([62, 72, 98, 226], radius=18, fill="#FFB6B9")
    draw.rounded_rectangle([104, 72, 140, 182], radius=18, fill="#8AC6D1")
    draw.rounded_rectangle([146, 72, 182, 140], radius=18, fill="#B8E0D2")
    draw.text((215, 82), "Things of Korean", font=FONTS["brand"], fill="#304047")
    draw.text((215, 158), title, font=FONTS["title"], fill="#263238")


def draw_footer(draw):
    draw.text((80, 1278), "@Things of Korean", font=FONTS["footer"], fill="#68756E")
    draw.rounded_rectangle([790, 1272, 1000, 1313], radius=20, fill="#FFFFFF")
    draw.text((822, 1279), "save & review", font=FONTS["footer"], fill="#6E5BC8")


def render_vocab(rows, output_path):
    img, draw = gradient()
    draw_header(draw, "TOPIK單字")
    palette = [("#2F7D6D", "#E1F4EE"), ("#7957C8", "#EEE8FF"), ("#D87966", "#FFE9E1")]
    left_x, right_x = 62, 555
    card_width, card_height = 463, 166
    top_y, gap_y = 310, 18

    for index, raw_item in enumerate(rows[:10]):
        item = display_vocab_row(raw_item)
        col, row = divmod(index, 5)
        x = left_x if col == 0 else right_x
        y = top_y + row * (card_height + gap_y)
        accent, tint = palette[index % len(palette)]
        draw.rounded_rectangle([x, y, x + card_width, y + card_height], radius=26, fill="#FFFFFF", outline="#DCE6DF", width=2)
        draw.rounded_rectangle([x + 20, y + 18, x + 122, y + 50], radius=16, fill=tint)
        draw.text((x + 38, y + 23), f"TOPIK {item['level']}", font=FONTS["tag"], fill=accent)
        draw.text((x + 386, y + 20), f"{index + 1:02d}", font=FONTS["num"], fill="#B3BDB6")

        word_font = FONTS["word_sm"] if len(item["word"]) >= 5 else FONTS["word"]
        draw.text((x + 20, y + 62), ellipsize(draw, item["word"], word_font, 175), font=word_font, fill="#263238")

        pos_text = f"{item['pos']} | "
        px, py = x + 210, y + 63
        draw.text((px, py), pos_text, font=FONTS["meta"], fill=accent)
        remaining_width = 225 - draw.textlength(pos_text, font=FONTS["meta"])
        draw_fit_line(
            draw,
            px + draw.textlength(pos_text, font=FONTS["meta"]),
            py,
            item["translation"],
            FONTS["meta"],
            "#263238",
            remaining_width,
            16,
        )

        draw_marker(draw, x + 22, y + 107, item["exampleKo"], item.get("highlight", item["word"]), 410, FONTS["ko"], "#4A5751")
        draw_fit_line(draw, x + 22, y + 132, translate_example(item), FONTS["zh"], "#7B8580", 410, 15)

    draw_footer(draw)
    img.save(output_path, quality=95)


def grammar_targets(pattern, sentence):
    if pattern == "-기 전에":
        return "기 전에"
    if pattern == "-는 동안":
        return "는 동안" if "는 동안" in sentence else "동안"
    if pattern == "-(으)ㄹ 만하다":
        for target in ["볼 만해요", "가 볼 만합니다", "을 만하다", "ㄹ 만하다", "만해요", "만합니다"]:
            if target in sentence:
                return target
    if pattern == "-(으)ㄹ 테니까":
        if "갈 테니까" in sentence:
            return "갈 테니까"
        if "막힐 테니까" in sentence:
            return "막힐 테니까"
    for chunk in pattern.replace("-", "").split("/"):
        if chunk and chunk in sentence:
            return chunk
    return ""


def draw_example(draw, x, y, sentence, translation, target, max_width):
    ko_width = draw.textlength(sentence, font=FONTS["ex_ko"])
    zh_text = f"  {translation}"
    zh_width = draw.textlength(zh_text, font=FONTS["ex_zh"])

    if ko_width + zh_width <= max_width:
        if target and target in sentence:
            pre, rest = sentence.split(target, 1)
            tx = x
            draw.text((tx, y), pre, font=FONTS["ex_ko"], fill="#263238")
            tx += draw.textlength(pre, font=FONTS["ex_ko"])
            target_width = draw.textlength(target, font=FONTS["ex_ko"])
            draw.rounded_rectangle([tx - 2, y + 17, tx + target_width + 3, y + 32], radius=6, fill=MARKER)
            draw.text((tx, y), target, font=FONTS["ex_ko"], fill="#263238")
            tx += target_width
            draw.text((tx, y), rest, font=FONTS["ex_ko"], fill="#263238")
            tx += draw.textlength(rest, font=FONTS["ex_ko"])
        else:
            draw.text((x, y), sentence, font=FONTS["ex_ko"], fill="#263238")
            tx = x + ko_width
        draw.text((tx, y + 3), zh_text, font=FONTS["ex_zh"], fill="#6F7B75")
        return y + 36

    draw_marker(draw, x, y, sentence, target, max_width, FONTS["ex_ko"], "#263238")
    draw_fit_line(draw, x, y + 34, translation, FONTS["ex_zh"], "#6F7B75", max_width, 18)
    return y + 58


def render_grammar(rows, output_path):
    img, draw = gradient((255, 249, 246), (241, 248, 247))
    draw_header(draw, "TOPIK文法")
    palette = [("#2F7D6D", "#E1F4EE"), ("#7957C8", "#EEE8FF")]
    ys = [286, 754]
    card_x, card_width, card_height = 62, 956, 463

    for index, item in enumerate(rows[:2]):
        accent, tint = palette[index % len(palette)]
        y = ys[index]
        draw.rounded_rectangle([card_x, y, card_x + card_width, y + card_height], radius=36, fill="#FFFFFF", outline="#DCE6DF", width=2)
        draw.rounded_rectangle([card_x + 34, y + 32, card_x + 178, y + 72], radius=20, fill=tint)
        draw.text((card_x + 57, y + 40), f"TOPIK {item['level']}", font=FONTS["tag"], fill=accent)

        pattern_font = FONTS["pattern_sm"] if len(item["pattern"]) >= 11 else FONTS["pattern"]
        draw.text((card_x + 34, y + 96), item["pattern"], font=pattern_font, fill="#263238")
        draw.rounded_rectangle([card_x + 34, y + 170, card_x + card_width - 34, y + 172], radius=1, fill="#EEF1EF")

        cy = y + 202
        draw.text((card_x + 34, cy), "接續", font=FONTS["label"], fill=accent)
        attachment_bottom = draw_fit_or_wrap(
            draw,
            card_x + 112,
            cy - 2,
            item.get("attachment", ""),
            FONTS["attach"],
            "#263238",
            790,
            2,
            17,
            5,
        )
        cy = max(cy + 54, attachment_bottom + 18)
        draw.text((card_x + 34, cy), "意思", font=FONTS["label"], fill=accent)
        cy = wrap(draw, item.get("meaning", ""), (card_x + 112, cy - 2), FONTS["body"], "#263238", 790, 2, 6) + 18

        for example_index, (sentence, translation) in enumerate(item.get("examples", [])[:2], start=1):
            draw.rounded_rectangle([card_x + 34, cy - 3, card_x + 94, cy + 35], radius=19, fill=tint)
            draw.text((card_x + 49, cy + 5), str(example_index), font=FONTS["tag"], fill=accent)
            target = grammar_targets(item["pattern"], sentence)
            cy = draw_example(draw, card_x + 118, cy - 2, sentence, translation, target, 785) + 8

    draw_footer(draw)
    img.save(output_path, quality=95)


def render_text(vocab_rows, grammar_rows, output_path):
    lines = [
        "TOPIK單字",
        "",
    ]
    for raw_item in vocab_rows[:10]:
        item = display_vocab_row(raw_item)
        lines.extend(
            [
                f"{item['word']}｜{item['translation']}",
                "",
            ]
        )

    lines.extend(
        [
            "",
            "TOPIK文法",
            "",
        ]
    )
    for item in grammar_rows[:2]:
        lines.extend(
            [
                f"TOPIK {item['level']}｜{item['pattern']}",
                f"意思：{item.get('meaning', '')}",
            ]
        )
        lines.append("")

    lines.extend(["@Things of Korean", ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    payload = json.loads(sys.stdin.read())
    date = payload["date"]
    output_dir = ROOT / "out" / "ig" / date
    output_dir.mkdir(parents=True, exist_ok=True)

    vocab_path = output_dir / f"topik-vocab-{date}.png"
    grammar_path = output_dir / f"topik-grammar-{date}.png"
    text_path = output_dir / f"topik-post-{date}.txt"
    render_vocab(payload["vocab"], vocab_path)
    render_grammar(payload["grammar"], grammar_path)
    render_text(payload["vocab"], payload["grammar"], text_path)

    print(vocab_path)
    print(grammar_path)
    print(text_path)


if __name__ == "__main__":
    main()
