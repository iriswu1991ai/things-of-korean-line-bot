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
        "exampleKo": "학교에서는 사고로 세상을 떠난 선생님을 추모하는 시간을 가졌어요.",
        "exampleZh": "學校舉行了悼念因事故過世老師的時間。",
        "highlight": "추모하는",
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
}


def display_vocab_row(row):
    override = VOCAB_OVERRIDES.get(row.get("word"))
    if override:
        return {**row, **override}
    word = row.get("word", "未知單字")
    raise ValueError(f"Missing curated vocabulary example for {word}. Add it to VOCAB_OVERRIDES before rendering.")


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
    shown = ellipsize(draw, text, font, max_width)
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
        draw.text((px + draw.textlength(pos_text, font=FONTS["meta"]), py), ellipsize(draw, item["translation"], FONTS["meta"], remaining_width), font=FONTS["meta"], fill="#263238")

        draw_marker(draw, x + 22, y + 107, item["exampleKo"], item.get("highlight", item["word"]), 410, FONTS["ko"], "#4A5751")
        wrap(draw, translate_example(item), (x + 22, y + 132), FONTS["zh"], "#7B8580", 410, 1, 2)

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
    return wrap(draw, translation, (x, y + 34), FONTS["ex_zh"], "#6F7B75", max_width, 1, 4)


def render_grammar(rows, output_path):
    img, draw = gradient((255, 249, 246), (241, 248, 247))
    draw_header(draw, "TOPIK文法")
    palette = [("#2F7D6D", "#E1F4EE"), ("#7957C8", "#EEE8FF")]
    ys = [292, 758]
    card_x, card_width, card_height = 62, 956, 445

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
        wrap(draw, item.get("attachment", ""), (card_x + 112, cy - 2), FONTS["attach"], "#263238", 790, 1, 5)
        cy += 61
        draw.text((card_x + 34, cy), "意思", font=FONTS["label"], fill=accent)
        cy = wrap(draw, item.get("meaning", ""), (card_x + 112, cy - 2), FONTS["body"], "#263238", 790, 2, 6) + 25

        for example_index, (sentence, translation) in enumerate(item.get("examples", [])[:2], start=1):
            draw.rounded_rectangle([card_x + 34, cy - 3, card_x + 94, cy + 35], radius=19, fill=tint)
            draw.text((card_x + 49, cy + 5), str(example_index), font=FONTS["tag"], fill=accent)
            target = grammar_targets(item["pattern"], sentence)
            cy = draw_example(draw, card_x + 118, cy - 2, sentence, translation, target, 785) + 16

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
