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


def load_font(path, size):
    for candidate in [path, FONT_ZH, FONT_ALL]:
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
    if TRANSLATE:
        try:
            translated = TRANSLATE(row["exampleKo"]).strip()
            if translated:
                return translated
        except Exception:
            pass
    return row.get("definitionZh") or ""


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
    if target not in shown:
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

    for index, item in enumerate(rows[:10]):
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

        draw_marker(draw, x + 22, y + 107, item["exampleKo"], item["word"], 410, FONTS["ko"], "#4A5751")
        wrap(draw, translate_example(item), (x + 22, y + 132), FONTS["zh"], "#7B8580", 410, 1, 2)

    draw_footer(draw)
    img.save(output_path, quality=95)


def grammar_targets(pattern, sentence):
    if pattern == "-기 전에":
        return "기 전에"
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


def main():
    payload = json.loads(sys.stdin.read())
    date = payload["date"]
    output_dir = ROOT / "out" / "ig" / date
    output_dir.mkdir(parents=True, exist_ok=True)

    vocab_path = output_dir / f"topik-vocab-{date}.png"
    grammar_path = output_dir / f"topik-grammar-{date}.png"
    render_vocab(payload["vocab"], vocab_path)
    render_grammar(payload["grammar"], grammar_path)

    print(vocab_path)
    print(grammar_path)


if __name__ == "__main__":
    main()
