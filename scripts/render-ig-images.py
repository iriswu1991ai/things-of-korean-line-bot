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
    "붕괴": {
        "translation": "崩塌，坍塌，崩潰",
        "exampleKo": "오래된 창고 벽이 장마철에 붕괴될 위험이 있어서 바로 보수 공사를 시작했어요.",
        "exampleZh": "那座老倉庫的牆壁在梅雨季有崩塌風險，所以我們立刻開始修繕工程。",
        "highlight": "붕괴될",
    },
    "함께": {
        "translation": "一起，共同，與共",
        "exampleKo": "팀원들과 함께 자료를 검토하니 실수가 훨씬 빨리 보여서 좋았어요.",
        "exampleZh": "和組員一起檢查資料時，錯誤很快就被找出來了，感覺很好。",
        "highlight": "함께",
    },
    "재료": {
        "translation": "材料",
        "exampleKo": "요리 수업 전에 재료를 미리 손질해 두면 실습이 훨씬 수월해요.",
        "exampleZh": "在料理課之前先把材料預先處理好，實作會順利很多。",
        "highlight": "재료를",
    },
    "공개": {
        "translation": "公開",
        "exampleKo": "학교는 행사 포스터를 공개한 뒤 신청 방법도 바로 안내했어요.",
        "exampleZh": "學校公開活動海報之後，也立刻說明了報名方式。",
        "highlight": "공개한",
    },
    "입구": {
        "translation": "入口",
        "exampleKo": "지하철 입구가 공사 중이라서 저는 옆 출구로 돌아갔어요.",
        "exampleZh": "因為地鐵入口正在施工，所以我繞到旁邊的出口去了。",
        "highlight": "입구가",
    },
    "변경하다": {
        "translation": "變更，改動",
        "exampleKo": "회의 시간이 겹쳐서 예약 시간을 오후로 변경했어요.",
        "exampleZh": "因為會議時間衝突，我把預約時間改到下午了。",
        "highlight": "변경했어요",
    },
    "실망하다": {
        "translation": "失望",
        "exampleKo": "결과를 보고 실망했지만 다음 시험은 더 잘 준비하기로 했어요.",
        "exampleZh": "看到結果後雖然失望，但我決定把下一次考試準備得更好。",
        "highlight": "실망했지만",
    },
    "편하다": {
        "translation": "舒服，舒暢",
        "exampleKo": "새 운동화가 발에 잘 맞아서 하루 종일 걸어도 정말 편했어요.",
        "exampleZh": "新運動鞋很合腳，所以我走了一整天也真的很舒服。",
        "highlight": "편했어요",
    },
    "철수하다": {
        "translation": "撤回，撤離，撤退，收起",
        "exampleKo": "비가 너무 세게 와서 행사팀은 장비를 먼저 철수했어요.",
        "exampleZh": "因為雨下得太大，活動團隊先把器材撤收了。",
        "highlight": "철수했어요",
    },
    "입다": {
        "translation": "穿",
        "exampleKo": "면접 날에는 단정한 셔츠를 입는 게 마음이 편해요.",
        "exampleZh": "面試那天穿整潔的襯衫會讓人心裡比較踏實。",
        "highlight": "입는",
    },
    "줄다": {
        "translation": "縮小，減少，減輕",
        "exampleKo": "야근이 줄어서 이번 달에는 저녁을 집에서 먹는 날이 많아요.",
        "exampleZh": "因為加班減少了，這個月在家吃晚餐的日子變多了。",
        "highlight": "줄어서",
    },
    "삭제하다": {
        "translation": "刪除",
        "exampleKo": "팀장님이 확인한 뒤에 중복된 파일은 바로 삭제했어요.",
        "exampleZh": "組長確認後，我立刻刪掉了重複的檔案。",
        "highlight": "삭제했어요",
    },
    "효율적": {
        "translation": "有效的，高效的",
        "exampleKo": "회의 자료를 미리 공유하면 회의가 훨씬 효율적이에요.",
        "exampleZh": "如果提前分享會議資料，會議就會高效得多。",
        "highlight": "효율적이에요",
    },
    "오늘": {
        "translation": "今天，今日",
        "exampleKo": "오늘은 마감이 있어서 점심도 책상에서 간단히 먹었어요.",
        "exampleZh": "今天因為要趕截止，我連午餐都在桌前簡單吃了。",
        "highlight": "오늘은",
    },
    "글자": {
        "translation": "字，文字",
        "exampleKo": "신입사원 교육 자료의 글자가 너무 작아서 저는 폰트 크기를 다시 조정했어요.",
        "exampleZh": "新人員工教育資料的字太小了，所以我重新調整了字體大小。",
        "highlight": "글자가",
    },
    "새사람": {
        "translation": "新媳婦，新娘子，新人",
        "exampleKo": "민수 씨는 새사람을 동료들에게 소개하면서 회사 생활을 잘 도와달라고 했어요.",
        "exampleZh": "民秀在把新婚妻子介紹給同事時，請大家多多幫助她適應公司生活。",
        "highlight": "새사람을",
    },
    "도달하다": {
        "translation": "到達",
        "exampleKo": "회의 자료를 정리하는 데 예상보다 시간이 걸려서 마감 전까지 겨우 도달했어요.",
        "exampleZh": "整理會議資料花了比預期更久的時間，所以我才勉強趕在截止前完成。",
        "highlight": "도달했어요",
    },
    "처형되다": {
        "translation": "被處刑，被判刑，被處決，被處死，被處以極刑",
        "exampleKo": "역사 수업에서 그 죄수는 공개 재판 뒤에 처형되었다고 배웠어요.",
        "exampleZh": "在歷史課上，我們學到那名囚犯是在公開審判後被處決的。",
        "highlight": "처형되었다고",
    },
    "시간": {
        "translation": "時間",
        "exampleKo": "회의 시간이 바뀌어서 저는 점심시간 전에 보고서를 먼저 끝냈어요.",
        "exampleZh": "會議時間改了，所以我在午休前先把報告完成了。",
        "highlight": "시간이",
    },
    "휴일": {
        "translation": "休息日，公休日，假日",
        "exampleKo": "휴일에도 병원 근무가 있어서 저는 아침 일찍 출근했어요.",
        "exampleZh": "就算是假日我也得在醫院值班，所以我一早就去上班了。",
        "highlight": "휴일에도",
    },
    "확인하다": {
        "translation": "確認，得知，檢視",
        "exampleKo": "출근 전에 이메일을 다시 확인하고 회의 자료를 챙겼어요.",
        "exampleZh": "上班前我又確認了一次電子郵件，並把會議資料帶上了。",
        "highlight": "확인하고",
    },
    "실망": {
        "translation": "失望",
        "exampleKo": "면접 결과가 좋지 않아서 저는 잠깐 실망했지만 바로 다시 준비했어요.",
        "exampleZh": "因為面試結果不理想，我一度很失望，但馬上又重新準備了。",
        "highlight": "실망했지만",
    },
    "입고되다": {
        "translation": "入庫，進貨",
        "exampleKo": "신제품이 오늘 오전에 입고되어서 매장 진열을 바로 시작했어요.",
        "exampleZh": "新產品今天上午已經進貨，所以我們立刻開始陳列到店裡。",
        "highlight": "입고되어서",
    },
    "위로하다": {
        "translation": "安慰，撫慰，慰藉",
        "exampleKo": "팀원이 발표를 망쳐서 저는 끝나고 커피를 사 주며 조용히 위로해 줬어요.",
        "exampleZh": "因為組員把發表搞砸了，我在結束後買了咖啡請他，安靜地安慰了他。",
        "highlight": "위로해 줬어요",
    },
    "제로": {
        "translation": "零",
        "exampleKo": "이번 달 신규 문의가 제로에 가까워서 팀에서 원인을 바로 점검했어요.",
        "exampleZh": "這個月的新詢問幾乎是零，所以團隊立刻檢查了原因。",
        "highlight": "제로에",
    },
    "논란": {
        "translation": "爭論，爭議",
        "exampleKo": "학교 급식 메뉴를 바꾸는 문제로 학부모들 사이에 논란이 생겼어요.",
        "exampleZh": "因為要更改學校營養午餐菜單，家長之間出現了爭議。",
        "highlight": "논란이",
    },
    "입법": {
        "translation": "立法",
        "exampleKo": "국회에서 입법 논의가 길어져서 새 제도 도입이 늦어졌어요.",
        "exampleZh": "國會的立法討論拖得很長，所以新制度的導入延後了。",
        "highlight": "입법 논의가",
    },
    "긴장": {
        "translation": "緊張",
        "exampleKo": "발표 직전에 긴장이 심해져서 저는 물을 천천히 마셨어요.",
        "exampleZh": "在發表前一刻緊張感變強，所以我慢慢喝了水。",
        "highlight": "긴장이",
    },
    "휴대폰": {
        "translation": "手機，行動電話，手提電話",
        "exampleKo": "수업 중에는 휴대폰을 가방에 넣어 두라는 안내를 받았어요.",
        "exampleZh": "上課時我們收到通知，手機要放在書包裡。",
        "highlight": "휴대폰을",
    },
    "검정색": {
        "translation": "黑色",
        "exampleKo": "면접 날에는 검정색 재킷을 입으면 좀 더 단정해 보여요.",
        "exampleZh": "面試那天穿黑色外套，看起來會更整潔。",
        "highlight": "검정색 재킷을",
    },
    "큰집": {
        "translation": "長房，老大家",
        "exampleKo": "명절마다 큰집에 모여서 식사 준비를 같이 해요.",
        "exampleZh": "每到節日我們都會聚到長房，一起準備餐點。",
        "highlight": "큰집에",
    },
    "뼈": {
        "translation": "骨，骨頭",
        "exampleKo": "오래 앉아 일했더니 허리뼈가 뻐근해서 스트레칭을 했어요.",
        "exampleZh": "久坐工作後，腰骨覺得僵硬，所以我做了伸展。",
        "highlight": "허리뼈가",
    },
    "정권": {
        "translation": "政權",
        "exampleKo": "선거 결과에 따라 정권이 바뀔 가능성이 있다는 이야기가 나왔어요.",
        "exampleZh": "有人提到，根據選舉結果，政權有可能更替。",
        "highlight": "정권이",
    },
    "호소": {
        "translation": "呼訴，訴苦，申訴，控訴",
        "exampleKo": "주민들은 밤늦은 공사 소음에 대해 시청에 호소했어요.",
        "exampleZh": "居民就深夜施工的噪音向市政府提出了申訴。",
        "highlight": "호소했어요",
    },
    "점심": {
        "translation": "中飯，午飯，午餐",
        "exampleKo": "회의가 길어져서 점심은 편의점 샌드위치로 간단히 해결했어요.",
        "exampleZh": "因為會議拖得很久，我就用便利商店三明治簡單解決了午餐。",
        "highlight": "점심은",
    },
    "가격": {
        "translation": "價格，價錢",
        "exampleKo": "장바구니에 담아 둔 채소 가격이 주말마다 달라서 미리 확인해요.",
        "exampleZh": "我放進購物籃的蔬菜價格每到週末都會變，所以我會先確認。",
        "highlight": "가격이",
    },
    "여권": {
        "translation": "護照",
        "exampleKo": "출장 전에 여권 유효기간을 꼭 다시 확인했어요.",
        "exampleZh": "出差前我一定會再確認護照有效期限。",
        "highlight": "여권",
    },
    "인간적": {
        "translation": "人的，人類的",
        "exampleKo": "그 선배는 실수해도 먼저 들어 주는 인간적인 사람이라서 믿음이 가요.",
        "exampleZh": "那位前輩即使犯錯也會先傾聽，是個很有人情味的人，所以讓人信任。",
        "highlight": "인간적인",
    },
    "돼지꿈": {
        "translation": "夢裡見豬，吉祥的夢",
        "exampleKo": "아침에 돼지꿈을 꾼 날은 괜히 기분이 좋아서 출근길이 가벼웠어요.",
        "exampleZh": "做了豬夢的那天，莫名心情特別好，連上班路都覺得輕快。",
        "highlight": "돼지꿈을",
    },
    "번역어": {
        "translation": "翻譯語",
        "exampleKo": "보고서 번역어를 그대로 두면 어색해서 팀에서 표현을 다시 다듬었어요.",
        "exampleZh": "如果報告裡的翻譯語照原樣放著會很生硬，所以團隊又重新修飾了表達。",
        "highlight": "번역어를",
    },
    "공단": {
        "translation": "工團，工業園區",
        "exampleKo": "새 공장이 들어서는 공단 근처에는 아침마다 통근 버스가 많아요.",
        "exampleZh": "新工廠進駐的工業園區附近，早上通勤巴士很多。",
        "highlight": "공단",
    },
    "첫사랑": {
        "translation": "初戀",
        "exampleKo": "동창회에서 첫사랑 이야기가 나와서 다들 한참 웃었어요.",
        "exampleZh": "在同學會上聊到初戀的話題，大家都笑了很久。",
        "highlight": "첫사랑 이야기가",
    },
    "검토되다": {
        "translation": "被檢討，被研究，被研討",
        "exampleKo": "수정된 제안서는 팀장님에게 검토된 뒤 최종 공유됐어요.",
        "exampleZh": "修改後的提案書經過組長審閱後，才做了最終分享。",
        "highlight": "검토된",
    },
    "이": {
        "translation": "牙齒",
        "exampleKo": "점심시간에 이가 시려서 찬물을 천천히 마셨어요.",
        "exampleZh": "午餐時間牙齒很敏感，所以我慢慢喝了冰水。",
        "highlight": "이가",
    },
    "다": {
        "translation": "全，都",
        "exampleKo": "회의 자료를 다 확인한 뒤에 팀장님께 보냈어요.",
        "exampleZh": "我把會議資料全部確認完後，傳給了組長。",
        "highlight": "다",
    },
    "하다": {
        "translation": "做，幹",
        "exampleKo": "오늘은 보고서를 마무리하고 일찍 퇴근하려고 해요.",
        "exampleZh": "我今天想把報告完成後早點下班。",
        "highlight": "하려고 해요",
    },
    "한": {
        "translation": "一",
        "exampleKo": "점심시간에 한 시간 정도 회의실을 비워 두었어요.",
        "exampleZh": "午餐時間我把會議室空出大約一小時。",
        "highlight": "한 시간",
    },
    "도": {
        "translation": "道理，道義",
        "exampleKo": "선배는 힘들어도 도리를 지키는 태도가 중요하다고 했어요.",
        "exampleZh": "前輩說即使辛苦，守住道義的態度也很重要。",
        "highlight": "도리를",
    },
    "있다": {
        "translation": "待著",
        "exampleKo": "저는 오전 내내 사무실에 있다가 점심에 나갔어요.",
        "exampleZh": "我整個上午都待在辦公室，中午才出去。",
        "highlight": "있다가",
    },
    "어": {
        "translation": "咦",
        "exampleKo": "어, 회의 시작 시간이 앞당겨졌네요.",
        "exampleZh": "咦，會議開始時間提前了。",
        "highlight": "어,",
    },
    "일": {
        "translation": "事情，工作",
        "exampleKo": "오늘 일은 다 끝내고 나서 집에 가요.",
        "exampleZh": "我把今天的工作都做完後再回家。",
        "highlight": "일은",
    },
    "나": {
        "translation": "我",
        "exampleKo": "나는 오늘 발표 준비를 마치고 일찍 퇴근할 거예요.",
        "exampleZh": "我今天會把簡報準備好，然後提早下班。",
        "highlight": "나는",
    },
    "지": {
        "translation": "從那時起，從那以後",
        "exampleKo": "이사한 지 두 달이 지나서야 회사 근처 길이 익숙해졌어요.",
        "exampleZh": "搬家兩個月後，我才終於熟悉公司附近的路。",
        "highlight": "지",
    },
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
    "답": {
        "translation": "回答，答話",
        "exampleKo": "회의에서 질문을 받았는데 바로 답을 하지 못했어요.",
        "exampleZh": "在會議上被問了問題，但我沒能立刻回答。",
        "highlight": "답을",
    },
    "화요일": {
        "translation": "星期二，週二，禮拜二",
        "exampleKo": "다음 주 화요일에 학교에서 학부모 회의가 있어요.",
        "exampleZh": "下週二學校有家長會。",
        "highlight": "화요일에",
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
    "셋째": {
        "translation": "第三次，第三個",
        "exampleKo": "이번이 셋째 발표라서 전보다 훨씬 덜 긴장했어요.",
        "exampleZh": "這是第三次發表，所以比之前沒那麼緊張。",
        "highlight": "셋째",
    },
    "관계하다": {
        "translation": "有關，涉足，參與",
        "exampleKo": "이 규정은 직원 복지와 관계하는 내용이에요.",
        "exampleZh": "這條規定和員工福利有關。",
        "highlight": "관계하는",
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
    "청소": {
        "translation": "打掃，清掃",
        "exampleKo": "퇴근 전에 책상 주변 청소를 간단히 했어요.",
        "exampleZh": "下班前我簡單打掃了書桌周圍。",
        "highlight": "청소를",
    },
    "현금": {
        "translation": "現金",
        "exampleKo": "시장에 갈 때는 현금을 조금 챙겨 가요.",
        "exampleZh": "去市場時我會帶一點現金。",
        "highlight": "현금을",
    },
    "과": {
        "translation": "科，部門",
        "exampleKo": "새로 옮긴 과에서 업무를 다시 배우고 있어요.",
        "exampleZh": "我在新調去的部門重新學習工作。",
        "highlight": "과에서",
    },
    "게": {
        "translation": "螃蟹",
        "exampleKo": "주말 저녁에는 가족들과 게 요리를 먹었어요.",
        "exampleZh": "週末晚上我和家人一起吃了螃蟹料理。",
        "highlight": "게",
    },
    "겨우": {
        "translation": "好不容易，勉強",
        "exampleKo": "아침 회의 시간에 겨우 맞춰 도착했어요.",
        "exampleZh": "我好不容易趕上了早上的會議時間。",
        "highlight": "겨우",
    },
    "절반": {
        "translation": "一半",
        "exampleKo": "보고서 수정은 오늘 절반 정도 끝냈어요.",
        "exampleZh": "報告修改今天大約完成了一半。",
        "highlight": "절반",
    },
    "나들이": {
        "translation": "出遊，外出走走",
        "exampleKo": "날씨가 좋아서 점심 후에 짧게 나들이를 갔어요.",
        "exampleZh": "天氣很好，所以午餐後短暫出去走走。",
        "highlight": "나들이를",
    },
    "이과": {
        "translation": "理科",
        "exampleKo": "동생은 이과 과목을 좋아해서 공학을 전공하고 싶어 해요.",
        "exampleZh": "弟弟喜歡理科科目，所以想主修工程。",
        "highlight": "이과",
    },
    "팀장": {
        "translation": "組長，主管",
        "exampleKo": "팀장이 일정 변경 내용을 단체 채팅방에 올렸어요.",
        "exampleZh": "組長把行程變更內容發到群組聊天室了。",
        "highlight": "팀장이",
    },
    "혈액": {
        "translation": "血液",
        "exampleKo": "건강 검진에서 혈액 검사 결과를 확인했어요.",
        "exampleZh": "健康檢查時我確認了血液檢查結果。",
        "highlight": "혈액",
    },
    "들다": {
        "translation": "進入，進去",
        "exampleKo": "회의실에 들자마자 발표 자료를 확인했어요.",
        "exampleZh": "一進會議室，我就確認了簡報資料。",
        "highlight": "들자마자",
    },
    "해": {
        "translation": "太陽",
        "exampleKo": "퇴근할 때 해가 아직 떠 있어서 기분이 좋았어요.",
        "exampleZh": "下班時太陽還沒下山，所以心情很好。",
        "highlight": "해가",
    },
    "나다": {
        "translation": "出現，發生",
        "exampleKo": "휴대폰에서 갑자기 알림 소리가 났어요.",
        "exampleZh": "手機突然響起了通知聲。",
        "highlight": "났어요",
    },
    "것": {
        "translation": "東西，事情",
        "exampleKo": "회의에서 중요한 것은 먼저 일정 확인이에요.",
        "exampleZh": "會議中重要的事情是先確認時程。",
        "highlight": "것은",
    },
    "수": {
        "translation": "方法，能力，可能",
        "exampleKo": "이 앱으로 출근 시간을 줄일 수 있어요.",
        "exampleZh": "用這個 App 可以減少通勤時間。",
        "highlight": "수",
    },
    "들리다": {
        "translation": "聽到，傳來",
        "exampleKo": "사무실 밖에서 웃음소리가 크게 들렸어요.",
        "exampleZh": "辦公室外傳來很大的笑聲。",
        "highlight": "들렸어요",
    },
    "긴장": {
        "translation": "緊張",
        "exampleKo": "면접 전에는 누구나 조금 긴장을 해요.",
        "exampleZh": "面試前誰都會有點緊張。",
        "highlight": "긴장을",
    },
    "북쪽": {
        "translation": "北邊，北方",
        "exampleKo": "회사 건물 북쪽에는 작은 공원이 있어요.",
        "exampleZh": "公司大樓北邊有一座小公園。",
        "highlight": "북쪽에는",
    },
    "선배": {
        "translation": "前輩",
        "exampleKo": "입사 첫날에 선배가 업무 순서를 알려 줬어요.",
        "exampleZh": "入職第一天，前輩告訴我工作流程。",
        "highlight": "선배가",
    },
    "결론": {
        "translation": "結論",
        "exampleKo": "긴 회의 끝에 드디어 결론이 나왔어요.",
        "exampleZh": "漫長會議結束後，終於有了結論。",
        "highlight": "결론이",
    },
    "굳이": {
        "translation": "一定，非得",
        "exampleKo": "바쁘면 굳이 오늘 답장하지 않아도 돼요.",
        "exampleZh": "如果忙，不一定要今天回覆也可以。",
        "highlight": "굳이",
    },
    "밟다": {
        "translation": "踩",
        "exampleKo": "비 오는 날에는 바닥의 물을 밟지 않게 조심해요.",
        "exampleZh": "下雨天要小心不要踩到地上的水。",
        "highlight": "밟지",
    },
    "북부": {
        "translation": "北部",
        "exampleKo": "출장 때문에 다음 주에는 북부 지역을 방문해요.",
        "exampleZh": "因為出差，下週會拜訪北部地區。",
        "highlight": "북부",
    },
    "응원": {
        "translation": "加油，應援",
        "exampleKo": "동료의 응원 덕분에 발표를 잘 마쳤어요.",
        "exampleZh": "多虧同事的加油，我順利完成了發表。",
        "highlight": "응원",
    },
    "지게": {
        "translation": "背架",
        "exampleKo": "박물관에서 옛날 사람들이 쓰던 지게를 봤어요.",
        "exampleZh": "我在博物館看到了以前人們使用的背架。",
        "highlight": "지게를",
    },
    "해로": {
        "translation": "海路",
        "exampleKo": "그 섬에는 해로를 이용해야 갈 수 있어요.",
        "exampleZh": "要去那座島必須走海路。",
        "highlight": "해로를",
    },
    "나들이하다": {
        "translation": "出遊，外出走走",
        "exampleKo": "주말에는 가족과 가까운 공원으로 나들이했어요.",
        "exampleZh": "週末我和家人到附近公園出遊。",
        "highlight": "나들이했어요",
    },
    "당해": {
        "translation": "該，本",
        "exampleKo": "당해 연도의 매출 자료를 다시 확인했어요.",
        "exampleZh": "我重新確認了該年度的銷售資料。",
        "highlight": "당해",
    },
    "자국": {
        "translation": "痕跡",
        "exampleKo": "책상 위에 컵 자국이 남아서 바로 닦았어요.",
        "exampleZh": "桌上留下杯痕，所以我馬上擦掉了。",
        "highlight": "자국이",
    },
    "출력": {
        "translation": "輸出，列印",
        "exampleKo": "회의 전에 발표 자료를 출력해 두세요.",
        "exampleZh": "會議前請先把簡報資料列印好。",
        "highlight": "출력해",
    },
    "학위": {
        "translation": "學位",
        "exampleKo": "그는 일을 하면서 대학원 학위를 준비하고 있어요.",
        "exampleZh": "他一邊工作，一邊準備研究所學位。",
        "highlight": "학위를",
    },
    "되다": {
        "translation": "成為，變成",
        "exampleKo": "꾸준히 연습하면 발표가 훨씬 자연스럽게 돼요.",
        "exampleZh": "持續練習的話，發表會變得自然很多。",
        "highlight": "돼요",
    },
    "안": {
        "translation": "裡面",
        "exampleKo": "가방 안에 여권과 지갑을 같이 넣어 두었어요.",
        "exampleZh": "我把護照和錢包一起放在包包裡。",
        "highlight": "안에",
    },
    "월": {
        "translation": "月",
        "exampleKo": "다음 월 회의 일정은 아직 정해지지 않았어요.",
        "exampleZh": "下個月的會議時程還沒有決定。",
        "highlight": "월",
    },
    "말": {
        "translation": "話，言語",
        "exampleKo": "상대방의 말을 끝까지 듣고 대답하는 게 좋아요.",
        "exampleZh": "把對方的話聽到最後再回答比較好。",
        "highlight": "말을",
    },
    "한글": {
        "translation": "韓文字母，韓文",
        "exampleKo": "처음에는 한글 자모부터 천천히 외웠어요.",
        "exampleZh": "一開始我先慢慢背韓文字母。",
        "highlight": "한글",
    },
    "끝내다": {
        "translation": "結束，完成",
        "exampleKo": "오늘 업무는 여섯 시 전에 끝내고 싶어요.",
        "exampleZh": "我想在六點前完成今天的工作。",
        "highlight": "끝내고",
    },
    "남기다": {
        "translation": "留下，剩下",
        "exampleKo": "회의가 끝난 뒤 질문을 메모로 남겼어요.",
        "exampleZh": "會議結束後，我把問題用筆記留下來。",
        "highlight": "남겼어요",
    },
    "열리다": {
        "translation": "開，打開",
        "exampleKo": "아침 아홉 시에 온라인 설명회가 열려요.",
        "exampleZh": "線上說明會在早上九點舉行。",
        "highlight": "열려요",
    },
    "긴장하다": {
        "translation": "緊張",
        "exampleKo": "첫 발표라서 조금 긴장했지만 잘 끝냈어요.",
        "exampleZh": "因為是第一次發表，所以有點緊張，但順利完成了。",
        "highlight": "긴장했지만",
    },
    "글자": {
        "translation": "字，文字",
        "exampleKo": "계약서의 작은 글자까지 꼼꼼히 확인했어요.",
        "exampleZh": "我連合約裡的小字都仔細確認了。",
        "highlight": "글자까지",
    },
    "보고": {
        "translation": "報告",
        "exampleKo": "팀장은 오전 회의에서 매출 보고를 했어요.",
        "exampleZh": "組長在上午會議做了銷售報告。",
        "highlight": "보고를",
    },
    "정기": {
        "translation": "定期",
        "exampleKo": "우리 팀은 매주 월요일에 정기 회의를 해요.",
        "exampleZh": "我們團隊每週一開定期會議。",
        "highlight": "정기",
    },
    "한마디": {
        "translation": "一句話",
        "exampleKo": "동료의 따뜻한 한마디에 힘이 났어요.",
        "exampleZh": "同事溫暖的一句話讓我有了力量。",
        "highlight": "한마디에",
    },
    "감상하다": {
        "translation": "欣賞，觀賞",
        "exampleKo": "퇴근 후에 친구와 전시를 감상했어요.",
        "exampleZh": "下班後我和朋友欣賞了展覽。",
        "highlight": "감상했어요",
    },
    "공공장소": {
        "translation": "公共場所",
        "exampleKo": "공공장소에서는 작은 목소리로 통화해요.",
        "exampleZh": "在公共場所要小聲講電話。",
        "highlight": "공공장소에서는",
    },
    "응원하다": {
        "translation": "加油，支持",
        "exampleKo": "친구들이 시험 전날까지 계속 응원해 줬어요.",
        "exampleZh": "朋友們一直支持我到考試前一天。",
        "highlight": "응원해",
    },
    "스마트하다": {
        "translation": "俐落的，端莊的",
        "exampleKo": "그는 면접 날 스마트한 정장을 입고 왔어요.",
        "exampleZh": "他面試那天穿著俐落的正裝來了。",
        "highlight": "스마트한",
    },
    "입고": {
        "translation": "入庫，進貨",
        "exampleKo": "인기 상품은 입고되자마자 바로 팔렸어요.",
        "exampleZh": "人氣商品一進貨就立刻賣掉了。",
        "highlight": "입고되자마자",
    },
    "우리다": {
        "translation": "泡出，熬出",
        "exampleKo": "아침에는 차를 진하게 우려서 마셔요.",
        "exampleZh": "早上我會把茶泡濃一點喝。",
        "highlight": "우려서",
    },
    "제로": {
        "translation": "零",
        "exampleKo": "이번 달 목표는 실수를 제로로 줄이는 거예요.",
        "exampleZh": "這個月的目標是把錯誤降到零。",
        "highlight": "제로로",
    },
    "참가자": {
        "translation": "參加者",
        "exampleKo": "강의 참가자에게는 자료를 메일로 보내 드려요.",
        "exampleZh": "我們會把資料用 email 寄給課程參加者。",
        "highlight": "참가자에게는",
    },
    "협정": {
        "translation": "協定",
        "exampleKo": "두 회사는 새 협정을 맺고 공동 프로젝트를 시작했어요.",
        "exampleZh": "兩家公司簽訂新協定後，開始了共同專案。",
        "highlight": "협정을",
    },
    "뇌세포": {
        "translation": "腦細胞",
        "exampleKo": "어려운 문제를 오래 생각하니 뇌세포를 다 쓴 기분이에요.",
        "exampleZh": "想困難問題想很久，感覺腦細胞都用完了。",
        "highlight": "뇌세포를",
    },
    "보급형": {
        "translation": "普及型，大眾型",
        "exampleKo": "회사에서는 직원용으로 보급형 노트북을 구매했어요.",
        "exampleZh": "公司為員工購買了普及型筆電。",
        "highlight": "보급형",
    },
    "확인되다": {
        "translation": "確認，得知",
        "exampleKo": "회의실 예약이 이미 확인되었는지 제가 다시 메일로 물어봤어요.",
        "exampleZh": "我又用電子郵件確認了會議室預約是不是已經確認好了。",
        "highlight": "확인되었는지",
    },
    "위로": {
        "translation": "慰勞，慰問",
        "exampleKo": "친구가 힘들어 보여서 점심시간에 위로의 메시지를 보냈어요.",
        "exampleZh": "因為朋友看起來很辛苦，所以我在午餐時間傳了慰問的訊息。",
        "highlight": "위로의",
    },
    "큰아기": {
        "translation": "大閨女，大兒媳，老大",
        "exampleKo": "명절마다 큰아기가 먼저 와서 부엌 일을 도와줬어요.",
        "exampleZh": "每逢節日，大媳婦總是先來幫忙廚房的事。",
        "highlight": "큰아기가",
    },
    "업소": {
        "translation": "小公司，營業所，店鋪",
        "exampleKo": "퇴근길에 동네 업소에서 필요한 우유를 사 왔어요.",
        "exampleZh": "我在下班路上到住家附近的店鋪買了需要的牛奶回來。",
        "highlight": "업소에서",
    },
    "있다": {
        "translation": "待著",
        "exampleKo": "점심시간에는 사무실에 있다가 근처 공원으로 잠깐 나갔어요.",
        "exampleZh": "午餐時間我先待在辦公室，然後短暫去附近公園走了一下。",
        "highlight": "있다가",
    },
    "외국어": {
        "translation": "外國語，外語",
        "exampleKo": "회사 회의에서 외국어를 써야 해서 발표 전에 미리 연습했어요.",
        "exampleZh": "因為公司會議上得使用外語，所以我在發表前先練習了。",
        "highlight": "외국어를",
    },
    "결과적": {
        "translation": "最終",
        "exampleKo": "회의를 두 번 더 한 덕분에 결과적으로 일정이 더 빨리 정리됐어요.",
        "exampleZh": "多開了兩次會議的結果，行程最後整理得更快了。",
        "highlight": "결과적으로",
    },
    "실망시키다": {
        "translation": "讓人失望，辜負",
        "exampleKo": "갑작스러운 일정 변경이 팀을 실망시켰지만 금방 대안을 찾았어요.",
        "exampleZh": "突然的行程變更讓團隊失望了，不過我們很快就找到了替代方案。",
        "highlight": "실망시켰지만",
    },
    "회원제": {
        "translation": "會員制",
        "exampleKo": "회사 근처 헬스장은 회원제로 운영돼서 미리 등록해야 해요.",
        "exampleZh": "公司附近的健身房是會員制經營，所以得先登記。",
        "highlight": "회원제로",
    },
    "광산": {
        "translation": "礦山",
        "exampleKo": "전시관에서 옛 광산에서 쓰던 도구를 직접 볼 수 있었어요.",
        "exampleZh": "在展示館裡可以親眼看到以前礦山使用的工具。",
        "highlight": "광산에서",
    },
    "년도": {
        "translation": "年度",
        "exampleKo": "올해는 예산이 줄어서 다음 년도 계획을 더 보수적으로 세우고 있어요.",
        "exampleZh": "因為今年預算縮減，我們正在把下一年度的計畫訂得更保守。",
        "highlight": "년도",
    },
    "자녀": {
        "translation": "子女",
        "exampleKo": "학부모 상담 날에는 자녀의 학교생활을 함께 이야기해요.",
        "exampleZh": "在家長諮詢日，我們會一起談孩子的學校生活。",
        "highlight": "자녀의",
    },
    "값하다": {
        "translation": "值得，對得起價格",
        "exampleKo": "이 중고 노트북은 성능이 좋아서 충분히 값하는 것 같아요.",
        "exampleZh": "這台二手筆電性能很好，我覺得很值得。",
        "highlight": "값하는",
    },
    "압도되다": {
        "translation": "被壓倒，被震撼",
        "exampleKo": "처음 본 대형 공연장 분위기에 저는 잠시 압도됐어요.",
        "exampleZh": "第一次看到大型表演場的氣氛時，我一度被震撼住了。",
        "highlight": "압도됐어요",
    },
    "높다": {
        "translation": "高，深厚",
        "exampleKo": "이 지역은 여름에도 습도가 높아서 에어컨을 자주 켜요.",
        "exampleZh": "這個地區就算在夏天濕度也很高，所以我常常開冷氣。",
        "highlight": "높아서",
    },
    "글쎄": {
        "translation": "這個嘛，嗯",
        "exampleKo": "글쎄, 이번 일정은 아직 확답을 못 받아서 다시 확인해야 해요.",
        "exampleZh": "這個嘛，這次的行程還沒拿到確定答覆，所以得再確認一次。",
        "highlight": "글쎄,",
    },
    "더하다": {
        "translation": "加，增加，添加",
        "exampleKo": "보고서에 최근 판매 수치를 더해서 다시 제출했어요.",
        "exampleZh": "我把最近的銷售數字加進報告後，再次提交了。",
        "highlight": "더해서",
    },
    "논의": {
        "translation": "討論，論議",
        "exampleKo": "회의에서는 새 근무 제도를 어떻게 바꿀지 논의가 길어졌어요.",
        "exampleZh": "在會議上，關於要怎麼調整新工作制度的討論拉長了。",
        "highlight": "논의가",
    },
    "접근법": {
        "translation": "接近法，方法",
        "exampleKo": "이 문제는 정면으로 밀어붙이는 접근법보다 차근차근 설명하는 방식이 더 잘 맞아요.",
        "exampleZh": "這個問題比起正面硬碰硬的做法，更適合用循序漸進說明的方式。",
        "highlight": "접근법보다",
    },
    "압도하다": {
        "translation": "壓倒，震撼",
        "exampleKo": "그 가수는 무대에만 서면 관객을 완전히 압도해요.",
        "exampleZh": "那位歌手只要站上舞台，就會完全震撼觀眾。",
        "highlight": "압도해요",
    },
    "면하다": {
        "translation": "面對，應付，避免",
        "exampleKo": "이번 주에는 팀 회의와 발표 준비를 동시에 면해야 해서 일정이 빠듯해요.",
        "exampleZh": "這週得同時應付團隊會議和簡報準備，所以行程很緊。",
        "highlight": "면해야",
    },
    "저가": {
        "translation": "低價，低價格",
        "exampleKo": "저가 항공권을 미리 사 두면 출장 비용을 많이 줄일 수 있어요.",
        "exampleZh": "如果先買好低價機票，可以大幅減少出差費用。",
        "highlight": "저가",
    },
    "협정하다": {
        "translation": "協定，簽訂協議",
        "exampleKo": "양쪽 회사는 새 계약 조건을 협정하기 위해 다시 만났어요.",
        "exampleZh": "雙方公司再次見面，是為了協定新的合約條件。",
        "highlight": "협정하기",
    },
    "좋다": {
        "translation": "好，適合，良好",
        "exampleKo": "지금은 날씨가 좋아서 점심 먹고 산책하기 딱 좋아요.",
        "exampleZh": "現在天氣很好，吃完午餐去散步正剛好。",
        "highlight": "좋아서",
    },
    "쌀": {
        "translation": "米，稻米",
        "exampleKo": "어머니는 아침마다 갓 지은 쌀밥을 챙겨 주셨어요.",
        "exampleZh": "媽媽每天早上都會幫我準備剛煮好的白飯。",
        "highlight": "쌀밥을",
    },
    "입력": {
        "translation": "輸入",
        "exampleKo": "비밀번호를 잘못 입력해서 로그인이 한 번 막혔어요.",
        "exampleZh": "因為密碼輸入錯誤，登入一度被擋住了。",
        "highlight": "입력해서",
    },
    "출력하다": {
        "translation": "輸出，列印",
        "exampleKo": "보고서를 출력해서 회의실 책상 위에 놓아 두었어요.",
        "exampleZh": "我把報告列印出來，放在會議室桌上了。",
        "highlight": "출력해서",
    },
    "없다": {
        "translation": "沒有",
        "exampleKo": "오늘은 오전 회의가 없어서 업무를 천천히 시작했어요.",
        "exampleZh": "今天上午沒有會議，所以我慢慢開始工作。",
        "highlight": "없어서",
    },
    "시계": {
        "translation": "鐘，錶",
        "exampleKo": "회의실 시계가 멈춰 있어서 시간을 잘못 봤어요.",
        "exampleZh": "會議室的鐘停了，所以我看錯時間。",
        "highlight": "시계가",
    },
    "씻다": {
        "translation": "洗",
        "exampleKo": "점심을 먹기 전에 손을 깨끗이 씻었어요.",
        "exampleZh": "吃午餐前我把手洗乾淨了。",
        "highlight": "씻었어요",
    },
    "점수": {
        "translation": "分數",
        "exampleKo": "이번 모의고사 점수가 지난번보다 조금 올랐어요.",
        "exampleZh": "這次模擬考分數比上次稍微提高了。",
        "highlight": "점수가",
    },
    "오랫동안": {
        "translation": "很久，長時間",
        "exampleKo": "오랫동안 준비한 발표라서 더 긴장됐어요.",
        "exampleZh": "因為是準備很久的發表，所以更緊張。",
        "highlight": "오랫동안",
    },
    "길이": {
        "translation": "長度",
        "exampleKo": "보고서 길이를 줄이려고 핵심 내용만 남겼어요.",
        "exampleZh": "為了縮短報告長度，我只留下重點內容。",
        "highlight": "길이를",
    },
    "근육": {
        "translation": "肌肉",
        "exampleKo": "오랜만에 운동했더니 다리 근육이 아파요.",
        "exampleZh": "久違地運動後，腿部肌肉很痛。",
        "highlight": "근육이",
    },
    "실망": {
        "translation": "失望",
        "exampleKo": "결과는 아쉬웠지만 크게 실망하지 않으려고 해요.",
        "exampleZh": "結果雖然可惜，但我不想太失望。",
        "highlight": "실망하지",
    },
    "질환": {
        "translation": "疾病，疾患",
        "exampleKo": "장시간 앉아 있으면 허리 질환이 생길 수 있어요.",
        "exampleZh": "長時間坐著可能會產生腰部疾病。",
        "highlight": "질환이",
    },
    "멀리멀리": {
        "translation": "遠遠地",
        "exampleKo": "주말에는 복잡한 일 생각을 멀리멀리 보내고 쉬었어요.",
        "exampleZh": "週末我把複雜的事情遠遠拋開，好好休息。",
        "highlight": "멀리멀리",
    },
    "옮다": {
        "translation": "轉移，移動",
        "exampleKo": "회의 장소가 큰 강의실로 옮아 갔어요.",
        "exampleZh": "會議地點移到大教室去了。",
        "highlight": "옮아",
    },
    "없어지다": {
        "translation": "消失，不見",
        "exampleKo": "파일을 정리하니까 책상 위의 서류 더미가 거의 없어졌어요.",
        "exampleZh": "整理檔案之後，桌上的文件堆幾乎都不見了。",
        "highlight": "없어졌어요",
    },
    "더하기": {
        "translation": "加法，加上",
        "exampleKo": "회의 자료에는 매출 더하기 비용 계산표가 들어 있어요.",
        "exampleZh": "會議資料裡有營收加上費用的計算表。",
        "highlight": "더하기",
    },
    "우리말": {
        "translation": "韓語，本國語",
        "exampleKo": "외국어 표현을 우리말로 자연스럽게 바꾸는 연습을 했어요.",
        "exampleZh": "我練習把外語表達自然地改成韓語。",
        "highlight": "우리말로",
    },
    "많아지다": {
        "translation": "變多，增加",
        "exampleKo": "프로젝트가 시작되면서 확인해야 할 일이 많아졌어요.",
        "exampleZh": "專案開始後，需要確認的事情變多了。",
        "highlight": "많아졌어요",
    },
    "가능하다": {
        "translation": "可能的，可行的",
        "exampleKo": "내일 오전에는 회의실 예약이 가능해요.",
        "exampleZh": "明天上午可以預約會議室。",
        "highlight": "가능해요",
    },
    "방송": {
        "translation": "廣播，電視節目",
        "exampleKo": "퇴근 후에는 한국어 방송을 들으면서 듣기 연습을 해요.",
        "exampleZh": "下班後我一邊聽韓語節目，一邊練習聽力。",
        "highlight": "방송을",
    },
    "권하다": {
        "translation": "建議，推薦",
        "exampleKo": "선생님은 모르는 단어를 예문과 함께 외우라고 권했어요.",
        "exampleZh": "老師建議把不懂的單字和例句一起背。",
        "highlight": "권했어요",
    },
    "시간적": {
        "translation": "時間的，時間上的",
        "exampleKo": "이번 주는 시간적 여유가 없어서 회의를 짧게 진행했어요.",
        "exampleZh": "這週時間上沒有餘裕，所以會議開得比較短。",
        "highlight": "시간적",
    },
    "입고되다": {
        "translation": "入庫，到貨",
        "exampleKo": "새 교재가 입고되면 바로 문자로 알려 드릴게요.",
        "exampleZh": "新教材到貨後，我會立刻用簡訊通知你。",
        "highlight": "입고되면",
    },
    "날로": {
        "translation": "日漸，日益",
        "exampleKo": "연습을 계속하니 발음이 날로 자연스러워지고 있어요.",
        "exampleZh": "持續練習後，發音日漸自然了。",
        "highlight": "날로",
    },
    "함께하다": {
        "translation": "一起做，共同參與",
        "exampleKo": "이번 프로젝트는 다른 부서와 함께해서 배울 점이 많았어요.",
        "exampleZh": "這次專案和其他部門一起做，所以學到很多。",
        "highlight": "함께해서",
    },
    "두고두고": {
        "translation": "久久地，長久地",
        "exampleKo": "첫 발표에서 받은 조언은 두고두고 도움이 됐어요.",
        "exampleZh": "第一次發表時得到的建議，之後長久地幫上了忙。",
        "highlight": "두고두고",
    },
    "볼만하다": {
        "translation": "值得看的，可看的",
        "exampleKo": "이번 전시회는 규모는 작지만 작품이 꽤 볼만해요.",
        "exampleZh": "這次展覽規模雖小，但作品相當值得看。",
        "highlight": "볼만해요",
    },
    "시간문제": {
        "translation": "時間問題",
        "exampleKo": "자료가 다 준비됐으니 발표 완성은 이제 시간문제예요.",
        "exampleZh": "資料都準備好了，完成發表現在只是時間問題。",
        "highlight": "시간문제예요",
    },
    "입다": {
        "translation": "穿",
        "exampleKo": "오늘 발표가 있어서 깔끔한 셔츠를 입었어요.",
        "exampleZh": "今天有發表，所以我穿了整潔的襯衫。",
        "highlight": "입었어요",
    },
    "생각": {
        "translation": "想法，思考",
        "exampleKo": "회의 전에 제 생각을 짧게 메모해 두었어요.",
        "exampleZh": "會議前我把自己的想法簡短記下來了。",
        "highlight": "생각을",
    },
    "받다": {
        "translation": "收到，得到",
        "exampleKo": "아침에 팀장님에게 확인 메일을 받았어요.",
        "exampleZh": "早上我收到了主管的確認信。",
        "highlight": "받았어요",
    },
    "좋아하다": {
        "translation": "喜歡",
        "exampleKo": "저는 퇴근 후에 조용한 카페에서 공부하는 것을 좋아해요.",
        "exampleZh": "我喜歡下班後在安靜的咖啡廳讀書。",
        "highlight": "좋아해요",
    },
    "먹다": {
        "translation": "吃",
        "exampleKo": "점심에는 동료들과 회사 근처에서 비빔밥을 먹었어요.",
        "exampleZh": "午餐我和同事在公司附近吃了拌飯。",
        "highlight": "먹었어요",
    },
    "만들다": {
        "translation": "製作，做",
        "exampleKo": "수업 자료를 보기 쉽게 표로 만들었어요.",
        "exampleZh": "我把上課資料做成容易閱讀的表格。",
        "highlight": "만들었어요",
    },
    "오늘": {
        "translation": "今天",
        "exampleKo": "오늘 회의는 오전 열 시에 시작해요.",
        "exampleZh": "今天的會議上午十點開始。",
        "highlight": "오늘",
    },
    "보다": {
        "translation": "看",
        "exampleKo": "퇴근 후에 한국 드라마를 보면서 듣기 연습을 했어요.",
        "exampleZh": "下班後我看韓劇練習聽力。",
        "highlight": "보면서",
    },
    "남자": {
        "translation": "男子，男人",
        "exampleKo": "저 남자는 우리 회사 새 직원이에요.",
        "exampleZh": "那位男生是我們公司的新員工。",
        "highlight": "남자는",
    },
    "집": {
        "translation": "家，房子",
        "exampleKo": "주말에는 집에서 밀린 공부를 했어요.",
        "exampleZh": "週末我在家補了之前沒讀完的書。",
        "highlight": "집에서",
    },
    "함께": {
        "translation": "一起，共同",
        "exampleKo": "동료들과 함께 점심을 먹으러 갔어요.",
        "exampleZh": "我和同事一起去吃午餐。",
        "highlight": "함께",
    },
    "차": {
        "translation": "茶",
        "exampleKo": "오후에는 따뜻한 차를 마시며 일을 정리했어요.",
        "exampleZh": "下午我一邊喝熱茶，一邊整理工作。",
        "highlight": "차를",
    },
    "길": {
        "translation": "路，道路",
        "exampleKo": "출근길에 길이 막혀서 조금 늦었어요.",
        "exampleZh": "上班路上塞車，所以我稍微遲到了。",
        "highlight": "길이",
    },
    "메일": {
        "translation": "電子郵件",
        "exampleKo": "회의 자료는 메일로 다시 보내 드릴게요.",
        "exampleZh": "會議資料我會再用 email 寄給你。",
        "highlight": "메일로",
    },
    "재료": {
        "translation": "材料",
        "exampleKo": "요리 수업 전에 필요한 재료를 미리 준비했어요.",
        "exampleZh": "料理課前我先準備好了需要的材料。",
        "highlight": "재료를",
    },
    "할인": {
        "translation": "折扣，優惠",
        "exampleKo": "서점에서 교재를 할인 가격으로 샀어요.",
        "exampleZh": "我在書店用折扣價買了教材。",
        "highlight": "할인",
    },
    "입구": {
        "translation": "入口",
        "exampleKo": "카페 입구에서 친구를 기다렸어요.",
        "exampleZh": "我在咖啡廳入口等朋友。",
        "highlight": "입구에서",
    },
    "날짜": {
        "translation": "日期",
        "exampleKo": "시험 날짜를 달력에 크게 표시해 두었어요.",
        "exampleZh": "我把考試日期大大標在月曆上。",
        "highlight": "날짜를",
    },
    "칭찬하다": {
        "translation": "稱讚，讚美",
        "exampleKo": "선생님은 발표를 잘한 학생을 칭찬했어요.",
        "exampleZh": "老師稱讚了發表做得好的學生。",
        "highlight": "칭찬했어요",
    },
    "존중하다": {
        "translation": "尊重",
        "exampleKo": "회의에서는 서로의 의견을 존중하는 태도가 중요해요.",
        "exampleZh": "會議中尊重彼此意見的態度很重要。",
        "highlight": "존중하는",
    },
    "안심하다": {
        "translation": "安心，放心",
        "exampleKo": "자료를 다시 확인하고 나서야 안심했어요.",
        "exampleZh": "重新確認資料後我才放心。",
        "highlight": "안심했어요",
    },
    "토론하다": {
        "translation": "討論",
        "exampleKo": "수업 시간에 환경 문제에 대해 토론했어요.",
        "exampleZh": "上課時我們討論了環境問題。",
        "highlight": "토론했어요",
    },
    "답변하다": {
        "translation": "答覆，回答",
        "exampleKo": "고객 문의에는 가능한 한 빨리 답변해야 해요.",
        "exampleZh": "客戶詢問要盡可能快點回覆。",
        "highlight": "답변해야",
    },
    "최신": {
        "translation": "最新",
        "exampleKo": "보고서에는 최신 통계를 넣어야 해요.",
        "exampleZh": "報告裡要放入最新統計。",
        "highlight": "최신",
    },
    "취향": {
        "translation": "喜好，品味",
        "exampleKo": "친구의 취향에 맞춰 생일 선물을 골랐어요.",
        "exampleZh": "我配合朋友的喜好挑了生日禮物。",
        "highlight": "취향에",
    },
    "원격": {
        "translation": "遠端",
        "exampleKo": "이번 주 회의는 원격으로 진행하기로 했어요.",
        "exampleZh": "這週會議決定以遠端方式進行。",
        "highlight": "원격으로",
    },
    "맥락": {
        "translation": "脈絡，前後文",
        "exampleKo": "문장을 이해하려면 앞뒤 맥락을 함께 봐야 해요.",
        "exampleZh": "要理解句子，就要一起看前後文脈絡。",
        "highlight": "맥락을",
    },
    "클라우드": {
        "translation": "雲端",
        "exampleKo": "중요한 파일은 클라우드에 백업해 두었어요.",
        "exampleZh": "重要檔案我備份到雲端了。",
        "highlight": "클라우드에",
    },
    "판매량": {
        "translation": "銷售量",
        "exampleKo": "신제품 판매량이 지난달보다 많이 늘었어요.",
        "exampleZh": "新產品銷售量比上個月增加很多。",
        "highlight": "판매량이",
    },
    "일관성": {
        "translation": "一致性",
        "exampleKo": "브랜드 이미지를 위해 디자인의 일관성을 지켜야 해요.",
        "exampleZh": "為了品牌形象，要維持設計的一致性。",
        "highlight": "일관성을",
    },
    "민감하다": {
        "translation": "敏感，敏銳",
        "exampleKo": "개인 정보는 민감한 내용이라 조심해서 다뤄야 해요.",
        "exampleZh": "個人資料是敏感內容，所以要小心處理。",
        "highlight": "민감한",
    },
    "또": {
        "translation": "又，再",
        "exampleKo": "내일 또 같은 시간에 회의가 있어요.",
        "exampleZh": "明天同一時間又有會議。",
        "highlight": "또",
    },
    "너무": {
        "translation": "太，非常",
        "exampleKo": "오늘은 일이 너무 많아서 조금 피곤해요.",
        "exampleZh": "今天工作太多，所以有點累。",
        "highlight": "너무",
    },
    "게임": {
        "translation": "遊戲，比賽",
        "exampleKo": "주말에는 친구들과 온라인 게임을 했어요.",
        "exampleZh": "週末我和朋友玩了線上遊戲。",
        "highlight": "게임을",
    },
    "줄다": {
        "translation": "減少，變少",
        "exampleKo": "회의 시간을 줄이려고 안건을 미리 정리했어요.",
        "exampleZh": "為了縮短會議時間，我先整理好了議題。",
        "highlight": "줄이려고",
    },
    "같이": {
        "translation": "一起，一同",
        "exampleKo": "퇴근 후에 동료와 같이 저녁을 먹었어요.",
        "exampleZh": "下班後我和同事一起吃了晚餐。",
        "highlight": "같이",
    },
    "샤워하다": {
        "translation": "淋浴，洗澡",
        "exampleKo": "운동이 끝난 후에 바로 샤워했어요.",
        "exampleZh": "運動結束後我馬上洗澡了。",
        "highlight": "샤워했어요",
    },
    "빌리다": {
        "translation": "借",
        "exampleKo": "도서관에서 한국어 책을 한 권 빌렸어요.",
        "exampleZh": "我在圖書館借了一本韓文書。",
        "highlight": "빌렸어요",
    },
    "농담하다": {
        "translation": "開玩笑",
        "exampleKo": "친구가 농담해서 회의 전 분위기가 가벼워졌어요.",
        "exampleZh": "朋友開了玩笑，會議前氣氛變輕鬆了。",
        "highlight": "농담해서",
    },
    "새롭다": {
        "translation": "新的，新鮮的",
        "exampleKo": "새로운 업무 방식을 배우는 중이에요.",
        "exampleZh": "我正在學新的工作方式。",
        "highlight": "새로운",
    },
    "멋있다": {
        "translation": "帥氣的，出色的",
        "exampleKo": "발표를 침착하게 하는 모습이 정말 멋있었어요.",
        "exampleZh": "冷靜發表的樣子真的很出色。",
        "highlight": "멋있었어요",
    },
    "한가하다": {
        "translation": "空閒的，悠閒的",
        "exampleKo": "오늘 오후는 비교적 한가해서 자료를 정리했어요.",
        "exampleZh": "今天下午比較空閒，所以整理了資料。",
        "highlight": "한가해서",
    },
    "갈등": {
        "translation": "矛盾，衝突",
        "exampleKo": "팀 안의 갈등을 줄이기 위해 의견을 들었어요.",
        "exampleZh": "為了減少團隊內的衝突，我聽取了意見。",
        "highlight": "갈등을",
    },
    "열정": {
        "translation": "熱情，幹勁",
        "exampleKo": "그는 새 프로젝트에 큰 열정을 보였어요.",
        "exampleZh": "他對新專案展現了很大的熱情。",
        "highlight": "열정을",
    },
    "확신": {
        "translation": "確信，信心",
        "exampleKo": "충분히 연습하니 합격할 수 있다는 확신이 생겼어요.",
        "exampleZh": "充分練習後，我產生了能合格的信心。",
        "highlight": "확신이",
    },
    "우려하다": {
        "translation": "擔憂，憂慮",
        "exampleKo": "팀장은 일정이 늦어질까 봐 우려했어요.",
        "exampleZh": "組長擔心時程會延後。",
        "highlight": "우려했어요",
    },
    "용서하다": {
        "translation": "原諒",
        "exampleKo": "친구는 제 실수를 이해하고 용서해 줬어요.",
        "exampleZh": "朋友理解並原諒了我的失誤。",
        "highlight": "용서해",
    },
    "봉사하다": {
        "translation": "服務，做志工",
        "exampleKo": "주말에는 지역 도서관에서 봉사했어요.",
        "exampleZh": "週末我在社區圖書館做志工。",
        "highlight": "봉사했어요",
    },
    "정교하다": {
        "translation": "精巧的，精密的",
        "exampleKo": "이 보고서는 분석이 정교해서 이해하기 쉬웠어요.",
        "exampleZh": "這份報告分析很精密，所以容易理解。",
        "highlight": "정교해서",
    },
    "완화하다": {
        "translation": "緩解，使緩和",
        "exampleKo": "회사는 업무 부담을 완화하기 위해 인원을 늘렸어요.",
        "exampleZh": "公司為了減輕工作負擔而增加人手。",
        "highlight": "완화하기",
    },
    "출동하다": {
        "translation": "出動，出勤",
        "exampleKo": "문제가 생기자 담당 직원이 바로 출동했어요.",
        "exampleZh": "一出問題，負責員工馬上出動了。",
        "highlight": "출동했어요",
    },
    "탐지하다": {
        "translation": "探測，偵測",
        "exampleKo": "새 시스템은 오류를 빠르게 탐지할 수 있어요.",
        "exampleZh": "新系統可以快速偵測錯誤。",
        "highlight": "탐지할",
    },
    "효력": {
        "translation": "效力，效果",
        "exampleKo": "새 규정은 다음 달부터 효력이 생겨요.",
        "exampleZh": "新規定從下個月開始生效。",
        "highlight": "효력이",
    },
    "최우선": {
        "translation": "最優先，第一位",
        "exampleKo": "이번 주에는 고객 응대를 최우선으로 처리해요.",
        "exampleZh": "這週我們把客戶應對列為最優先處理。",
        "highlight": "최우선으로",
    },
    "운항하다": {
        "translation": "運航，航行",
        "exampleKo": "태풍 때문에 일부 항공편이 운항하지 않아요.",
        "exampleZh": "因為颱風，部分航班沒有飛航。",
        "highlight": "운항하지",
    },
    "변경하다": {
        "translation": "變更，改動",
        "exampleKo": "회의 시간이 바뀌어서 일정을 변경했어요.",
        "exampleZh": "會議時間改了，所以我變更了行程。",
        "highlight": "변경했어요",
    },
    "취소하다": {
        "translation": "取消",
        "exampleKo": "비가 많이 와서 야외 수업을 취소했어요.",
        "exampleZh": "因為下大雨，所以取消了戶外課。",
        "highlight": "취소했어요",
    },
    "작성하다": {
        "translation": "撰寫，製作",
        "exampleKo": "오전에 회의록을 작성해서 팀에 공유했어요.",
        "exampleZh": "上午我寫好會議紀錄後分享給團隊。",
        "highlight": "작성해서",
    },
    "복사하다": {
        "translation": "影印，複製",
        "exampleKo": "수업 자료를 열 장 복사했어요.",
        "exampleZh": "我影印了十份上課資料。",
        "highlight": "복사했어요",
    },
    "삭제하다": {
        "translation": "刪除",
        "exampleKo": "잘못 보낸 파일은 바로 삭제했어요.",
        "exampleZh": "寄錯的檔案我馬上刪除了。",
        "highlight": "삭제했어요",
    },
    "완료하다": {
        "translation": "完成，結束",
        "exampleKo": "오늘 해야 할 업무를 모두 완료했어요.",
        "exampleZh": "今天該做的工作我都完成了。",
        "highlight": "완료했어요",
    },
    "출발하다": {
        "translation": "出發",
        "exampleKo": "늦지 않으려고 평소보다 일찍 출발했어요.",
        "exampleZh": "為了不遲到，我比平常更早出發。",
        "highlight": "출발했어요",
    },
    "확인하다": {
        "translation": "確認，檢查",
        "exampleKo": "메일을 보내기 전에 첨부 파일을 확인했어요.",
        "exampleZh": "寄 email 前我確認了附件。",
        "highlight": "확인했어요",
    },
    "비교하다": {
        "translation": "比較",
        "exampleKo": "두 자료를 비교해 보고 더 쉬운 방법을 골랐어요.",
        "exampleZh": "我比較兩份資料後選了更簡單的方法。",
        "highlight": "비교해",
    },
    "설명하다": {
        "translation": "說明，解釋",
        "exampleKo": "새 직원에게 업무 절차를 천천히 설명했어요.",
        "exampleZh": "我慢慢向新員工說明工作流程。",
        "highlight": "설명했어요",
    },
    "업무": {
        "translation": "業務，工作",
        "exampleKo": "이번 주에는 새로운 업무를 배우고 있어요.",
        "exampleZh": "這週我正在學新的工作內容。",
        "highlight": "업무를",
    },
    "목표": {
        "translation": "目標",
        "exampleKo": "올해 목표는 TOPIK 점수를 올리는 거예요.",
        "exampleZh": "今年的目標是提高 TOPIK 分數。",
        "highlight": "목표는",
    },
    "해결하다": {
        "translation": "解決",
        "exampleKo": "팀원들과 이야기해서 문제를 해결했어요.",
        "exampleZh": "我和組員討論後解決了問題。",
        "highlight": "해결했어요",
    },
    "실수": {
        "translation": "失誤，錯誤",
        "exampleKo": "작은 실수도 다시 확인하면 줄일 수 있어요.",
        "exampleZh": "小失誤只要再次確認就能減少。",
        "highlight": "실수도",
    },
    "필요하다": {
        "translation": "必要，需要",
        "exampleKo": "발표 전에 충분한 연습이 필요해요.",
        "exampleZh": "發表前需要充分練習。",
        "highlight": "필요해요",
    },
    "편하다": {
        "translation": "舒服，方便",
        "exampleKo": "이 앱은 사용하기 편해서 자주 써요.",
        "exampleZh": "這個 App 用起來很方便，所以我常用。",
        "highlight": "편해서",
    },
    "빠르다": {
        "translation": "快，迅速",
        "exampleKo": "아침에는 지하철이 버스보다 빨라요.",
        "exampleZh": "早上捷運比公車快。",
        "highlight": "빨라요",
    },
    "느리다": {
        "translation": "慢，緩慢",
        "exampleKo": "오늘은 인터넷이 느려서 파일 전송이 오래 걸렸어요.",
        "exampleZh": "今天網路很慢，所以傳檔花了很久。",
        "highlight": "느려서",
    },
    "어렵다": {
        "translation": "難，不容易",
        "exampleKo": "처음에는 어렵지만 계속 연습하면 익숙해져요.",
        "exampleZh": "一開始雖然難，但持續練習就會熟悉。",
        "highlight": "어렵지만",
    },
    "쉽다": {
        "translation": "容易，簡單",
        "exampleKo": "선생님 설명이 쉬워서 바로 이해했어요.",
        "exampleZh": "老師說明得很簡單，所以我馬上理解了。",
        "highlight": "쉬워서",
    },
    "피곤하다": {
        "translation": "疲倦，疲憊",
        "exampleKo": "어제 늦게 자서 오늘은 조금 피곤해요.",
        "exampleZh": "昨天很晚睡，所以今天有點累。",
        "highlight": "피곤해요",
    },
    "깨끗하다": {
        "translation": "乾淨，整潔",
        "exampleKo": "회의실을 깨끗하게 정리하고 나왔어요.",
        "exampleZh": "我把會議室整理乾淨後才離開。",
        "highlight": "깨끗하게",
    },
    "친절하다": {
        "translation": "親切，友善",
        "exampleKo": "안내 직원이 친절해서 길을 쉽게 찾았어요.",
        "exampleZh": "服務人員很親切，所以我很快找到路。",
        "highlight": "친절해서",
    },
    "충분하다": {
        "translation": "充分，足夠",
        "exampleKo": "자료가 충분해서 보고서를 쓰기 쉬웠어요.",
        "exampleZh": "資料很充分，所以報告很好寫。",
        "highlight": "충분해서",
    },
    "성과": {
        "translation": "成果，成效",
        "exampleKo": "이번 프로젝트는 기대보다 좋은 성과를 냈어요.",
        "exampleZh": "這次專案做出了比預期更好的成果。",
        "highlight": "성과를",
    },
    "분석하다": {
        "translation": "分析",
        "exampleKo": "설문 결과를 분석해서 보고서에 넣었어요.",
        "exampleZh": "我分析問卷結果後放進報告裡。",
        "highlight": "분석해서",
    },
    "관리하다": {
        "translation": "管理",
        "exampleKo": "팀장은 전체 일정을 꼼꼼히 관리했어요.",
        "exampleZh": "組長仔細管理了整體時程。",
        "highlight": "관리했어요",
    },
    "보고서": {
        "translation": "報告書",
        "exampleKo": "퇴근 전에 보고서를 팀장님께 보냈어요.",
        "exampleZh": "下班前我把報告寄給了組長。",
        "highlight": "보고서를",
    },
    "협력하다": {
        "translation": "合作，協力",
        "exampleKo": "다른 부서와 협력해서 행사를 준비했어요.",
        "exampleZh": "我和其他部門合作準備活動。",
        "highlight": "협력해서",
    },
    "효율": {
        "translation": "效率，效能",
        "exampleKo": "업무 효율을 높이려고 회의 시간을 줄였어요.",
        "exampleZh": "為了提高工作效率，我縮短了會議時間。",
        "highlight": "효율을",
    },
    "효율적": {
        "translation": "有效率的，高效的",
        "exampleKo": "이 방법이 더 효율적이라서 팀에서 바로 적용했어요.",
        "exampleZh": "這個方法更有效率，所以團隊馬上採用了。",
        "highlight": "효율적이라서",
    },
    "적극적": {
        "translation": "積極的",
        "exampleKo": "그는 회의에서 적극적으로 의견을 냈어요.",
        "exampleZh": "他在會議中積極提出意見。",
        "highlight": "적극적으로",
    },
    "담당하다": {
        "translation": "負責，擔任",
        "exampleKo": "이번 달부터 고객 상담 업무를 담당하게 됐어요.",
        "exampleZh": "從這個月開始我負責客戶諮詢工作。",
        "highlight": "담당하게",
    },
    "참석하다": {
        "translation": "參加，出席",
        "exampleKo": "내일 오전 회의에는 모든 팀원이 참석해요.",
        "exampleZh": "明天上午的會議所有組員都會出席。",
        "highlight": "참석해요",
    },
    "축소하다": {
        "translation": "縮小，縮減",
        "exampleKo": "예산이 줄어서 행사 규모를 축소했어요.",
        "exampleZh": "因為預算減少，所以縮小了活動規模。",
        "highlight": "축소했어요",
    },
    "증가하다": {
        "translation": "增加",
        "exampleKo": "온라인 주문이 지난달보다 증가했어요.",
        "exampleZh": "線上訂單比上個月增加了。",
        "highlight": "증가했어요",
    },
    "예상하다": {
        "translation": "預想，預料",
        "exampleKo": "팀은 다음 달 매출이 늘어날 것으로 예상했어요.",
        "exampleZh": "團隊預估下個月營收會增加。",
        "highlight": "예상했어요",
    },
    "환경": {
        "translation": "環境",
        "exampleKo": "조용한 환경에서 공부하면 집중이 잘돼요.",
        "exampleZh": "在安靜的環境讀書時比較能集中。",
        "highlight": "환경에서",
    },
    "조건": {
        "translation": "條件",
        "exampleKo": "계약 조건을 다시 확인한 뒤 서명했어요.",
        "exampleZh": "我重新確認合約條件後才簽名。",
        "highlight": "조건을",
    },
    "의견": {
        "translation": "意見",
        "exampleKo": "회의에서 각자의 의견을 자유롭게 말했어요.",
        "exampleZh": "會議中大家自由地說出各自的意見。",
        "highlight": "의견을",
    },
    "활약하다": {
        "translation": "活躍，表現出色",
        "exampleKo": "그 직원은 새 프로젝트에서 크게 활약했어요.",
        "exampleZh": "那位員工在新專案中表現很出色。",
        "highlight": "활약했어요",
    },
    "중대하다": {
        "translation": "重大的，重要的",
        "exampleKo": "이번 결정은 회사에 중대한 영향을 줄 수 있어요.",
        "exampleZh": "這次決定可能會對公司造成重大影響。",
        "highlight": "중대한",
    },
    "채팅하다": {
        "translation": "聊天，線上聊天",
        "exampleKo": "퇴근 후 친구와 잠깐 채팅했어요.",
        "exampleZh": "下班後我和朋友線上聊了一下。",
        "highlight": "채팅했어요",
    },
    "합류하다": {
        "translation": "加入，會合",
        "exampleKo": "새로운 디자이너가 다음 주부터 팀에 합류해요.",
        "exampleZh": "新的設計師從下週開始加入團隊。",
        "highlight": "합류해요",
    },
    "추구하다": {
        "translation": "追求",
        "exampleKo": "우리 팀은 빠른 속도보다 정확한 결과를 추구해요.",
        "exampleZh": "我們團隊比起速度，更追求正確的結果。",
        "highlight": "추구해요",
    },
    "특이하다": {
        "translation": "特別的，特殊的",
        "exampleKo": "그 카페는 분위기가 특이해서 기억에 남아요.",
        "exampleZh": "那間咖啡廳氣氛很特別，所以讓人印象深刻。",
        "highlight": "특이해서",
    },
    "복구하다": {
        "translation": "恢復，修復",
        "exampleKo": "담당자가 삭제된 파일을 다시 복구했어요.",
        "exampleZh": "負責人把被刪除的檔案恢復了。",
        "highlight": "복구했어요",
    },
    "규제하다": {
        "translation": "限制，管制",
        "exampleKo": "회사는 보안을 위해 외부 접속을 규제했어요.",
        "exampleZh": "公司為了安全限制了外部連線。",
        "highlight": "규제했어요",
    },
    "파견하다": {
        "translation": "派遣",
        "exampleKo": "본사는 전문가를 현장에 파견했어요.",
        "exampleZh": "總公司派遣專家到現場。",
        "highlight": "파견했어요",
    },
    "철저하다": {
        "translation": "徹底的，周密的",
        "exampleKo": "중요한 발표 전에는 철저한 준비가 필요해요.",
        "exampleZh": "重要發表前需要周密準備。",
        "highlight": "철저한",
    },
    "논의하다": {
        "translation": "討論，研議",
        "exampleKo": "팀은 다음 달 계획을 자세히 논의했어요.",
        "exampleZh": "團隊詳細討論了下個月的計畫。",
        "highlight": "논의했어요",
    },
    "입력하다": {
        "translation": "輸入，登錄",
        "exampleKo": "신청서를 작성한 뒤 정보를 시스템에 입력했어요.",
        "exampleZh": "填完申請書後，我把資料輸入系統。",
        "highlight": "입력했어요",
    },
    "실망하다": {
        "translation": "失望",
        "exampleKo": "결과는 아쉬웠지만 너무 실망하지 않기로 했어요.",
        "exampleZh": "結果雖然可惜，但我決定不要太失望。",
        "highlight": "실망하지",
    },
    "존경하다": {
        "translation": "尊敬",
        "exampleKo": "저는 책임감 있게 일하는 선배를 존경해요.",
        "exampleZh": "我尊敬有責任感工作的前輩。",
        "highlight": "존경해요",
    },
    "평등하다": {
        "translation": "平等",
        "exampleKo": "모든 직원에게 평등한 기회를 주는 것이 중요해요.",
        "exampleZh": "給所有員工平等的機會很重要。",
        "highlight": "평등한",
    },
    "응답하다": {
        "translation": "回應，回答",
        "exampleKo": "고객의 문의에 빠르게 응답했어요.",
        "exampleZh": "我快速回應了客戶的詢問。",
        "highlight": "응답했어요",
    },
    "확신하다": {
        "translation": "確信，確定",
        "exampleKo": "충분히 확인한 뒤에야 결과를 확신했어요.",
        "exampleZh": "充分確認後，我才確定結果。",
        "highlight": "확신했어요",
    },
    "적응하다": {
        "translation": "適應",
        "exampleKo": "새로운 업무 방식에 조금씩 적응하고 있어요.",
        "exampleZh": "我正在慢慢適應新的工作方式。",
        "highlight": "적응하고",
    },
    "당황하다": {
        "translation": "慌張，驚慌",
        "exampleKo": "갑자기 질문을 받아서 조금 당황했어요.",
        "exampleZh": "突然被問問題，所以我有點慌張。",
        "highlight": "당황했어요",
    },
    "설득하다": {
        "translation": "說服",
        "exampleKo": "팀장은 자료를 보여 주며 고객을 설득했어요.",
        "exampleZh": "組長一邊展示資料，一邊說服客戶。",
        "highlight": "설득했어요",
    },
    "협조하다": {
        "translation": "協助，配合",
        "exampleKo": "모두가 협조해서 행사를 무사히 마쳤어요.",
        "exampleZh": "大家互相配合，順利完成了活動。",
        "highlight": "협조해서",
    },
    "중대성": {
        "translation": "重要性，重大性",
        "exampleKo": "보안 문제의 중대성을 모두에게 설명했어요.",
        "exampleZh": "我向大家說明了資安問題的重要性。",
        "highlight": "중대성을",
    },
    "압박하다": {
        "translation": "施壓，壓迫",
        "exampleKo": "무리한 일정은 팀원들을 압박할 수 있어요.",
        "exampleZh": "不合理的時程可能會壓迫組員。",
        "highlight": "압박할",
    },
    "침입하다": {
        "translation": "入侵，闖入",
        "exampleKo": "외부인이 사무실에 침입하지 못하도록 문을 잠갔어요.",
        "exampleZh": "為了不讓外人闖入辦公室，我鎖上了門。",
        "highlight": "침입하지",
    },
    "탈퇴하다": {
        "translation": "退出，退會",
        "exampleKo": "사용하지 않는 서비스는 이번 달에 탈퇴했어요.",
        "exampleZh": "這個月我退出了不用的服務。",
        "highlight": "탈퇴했어요",
    },
    "대결하다": {
        "translation": "對決，較量",
        "exampleKo": "두 팀은 결승전에서 다시 대결했어요.",
        "exampleZh": "兩隊在決賽中再次對決。",
        "highlight": "대결했어요",
    },
    "착용하다": {
        "translation": "穿戴，佩戴",
        "exampleKo": "회의장에서는 직원증을 꼭 착용해야 해요.",
        "exampleZh": "在會議場必須佩戴員工證。",
        "highlight": "착용해야",
    },
    "명성": {
        "translation": "名聲，聲望",
        "exampleKo": "그 회사는 좋은 서비스로 명성을 얻었어요.",
        "exampleZh": "那家公司以良好的服務獲得名聲。",
        "highlight": "명성을",
    },
    "복원하다": {
        "translation": "復原，修復",
        "exampleKo": "백업 파일로 중요한 자료를 복원했어요.",
        "exampleZh": "我用備份檔復原了重要資料。",
        "highlight": "복원했어요",
    },
    "양도하다": {
        "translation": "轉讓",
        "exampleKo": "사용하지 않는 장비를 다른 부서에 양도했어요.",
        "exampleZh": "我把不用的設備轉讓給其他部門。",
        "highlight": "양도했어요",
    },
    "집착하다": {
        "translation": "執著，固執",
        "exampleKo": "한 가지 방법에만 집착하지 말고 다른 방법도 생각해 봐요.",
        "exampleZh": "不要只執著於一種方法，也想想其他方法吧。",
        "highlight": "집착하지",
    },
    "협박하다": {
        "translation": "威脅，脅迫",
        "exampleKo": "상대를 협박하는 말은 절대 하면 안 돼요.",
        "exampleZh": "絕對不能說威脅對方的話。",
        "highlight": "협박하는",
    },
    "도덕적": {
        "translation": "道德的",
        "exampleKo": "회사는 도덕적인 기준을 지키려고 노력해요.",
        "exampleZh": "公司努力遵守道德標準。",
        "highlight": "도덕적인",
    },
    "총괄하다": {
        "translation": "總管，統籌",
        "exampleKo": "팀장님이 이번 프로젝트 전체를 총괄해요.",
        "exampleZh": "組長統籌這次整個專案。",
        "highlight": "총괄해요",
    },
    "철수하다": {
        "translation": "撤回，撤離",
        "exampleKo": "행사가 끝난 뒤 장비를 모두 철수했어요.",
        "exampleZh": "活動結束後，我們撤走了所有設備。",
        "highlight": "철수했어요",
    },
    "추락하다": {
        "translation": "墜落，跌落",
        "exampleKo": "나쁜 후기 때문에 브랜드 이미지가 추락했어요.",
        "exampleZh": "因為負評，品牌形象下滑了。",
        "highlight": "추락했어요",
    },
    "회전하다": {
        "translation": "旋轉，迴轉",
        "exampleKo": "화면이 자동으로 회전해서 보기 편했어요.",
        "exampleZh": "畫面會自動旋轉，所以看起來很方便。",
        "highlight": "회전해서",
    },
    "발굴하다": {
        "translation": "發掘，挖掘",
        "exampleKo": "회사는 새로운 인재를 발굴하기 위해 공모전을 열었어요.",
        "exampleZh": "公司為了發掘新人才而舉辦了徵選。",
        "highlight": "발굴하기",
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
                f"TOPIK {item['level']}｜{item['word']}｜{item['translation']}",
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
