#!/usr/bin/env python3
"""Render the animated, GitHub-compatible GIF banners for the profile README."""

from math import cos, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = (7, 11, 20)
PANEL = (14, 21, 37)
LINE = (47, 65, 100)
BLUE = (40, 87, 255)
BLUE_LIGHT = (111, 159, 255)
ICE = (215, 232, 255)
INK = (245, 245, 238)
MUTED = (155, 173, 208)
GRID = (15, 22, 36)


def font(size, bold=False, mono=False, impact=False):
    if impact:
        options = ["C:/Windows/Fonts/impact.ttf"]
    elif mono:
        options = ["C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    else:
        options = ["C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for candidate in options:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def base(size, kicker, right="SAMEER8549", color=NAVY):
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, size[0], 7), fill=BLUE)
    if color == NAVY:
        for x in range(0, size[0], 32):
            draw.line((x, 7, x, size[1]), fill=GRID, width=1)
        for y in range(7, size[1], 32):
            draw.line((0, y, size[0], y), fill=GRID, width=1)
    draw.text((38, 20), kicker, font=font(12, mono=True), fill=ICE)
    draw.text((size[0] - 38, 20), right, font=font(12, mono=True), fill=MUTED, anchor="ra")
    return image


def save_gif(name, frames, duration=100):
    frames[0].save(ASSETS / f"{name}.gif", save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True, disposal=2)


def animate_hero():
    source = Image.open(ASSETS / "hero.gif")
    source_frames = []
    for i in range(source.n_frames):
        source.seek(i)
        source_frames.append(source.convert("RGB"))
    frames = []
    for i in range(24):
        image = source_frames[i].copy()
        px = image.load()
        strength = (1 - cos(i / 24 * tau)) / 2
        target = tuple(round(a + (b - a) * strength) for a, b in zip(BLUE, ICE))
        # Let the surname's royal-blue ink breathe while the original project ribbon moves.
        for y in range(218, 315):
            for x in range(28, 540):
                r, g, b = px[x, y]
                if b > 130 and b > r * 1.45 and g < 190:
                    luminance = max(0.58, min(1.0, b / 255))
                    px[x, y] = tuple(round(c * luminance) for c in target)
        # Role signal flashes with the same identity pulse, beyond the moving ribbon.
        for y in range(326, 351):
            for x in range(38, 274):
                r, g, b = px[x, y]
                if b > 130 and b > r * 1.3:
                    px[x, y] = tuple(round(c * (0.7 + 0.3 * strength)) for c in ICE)
        frames.append(image)
    save_gif("hero", frames, duration=90)


def about_panel():
    w, h = 1200, 370
    frames = []
    stages = [("SEE", "VISION / SIGNAL"), ("REASON", "MODELS / CONTEXT"),
              ("CONNECT", "API / DATA"), ("SHIP", "PRODUCT / PEOPLE")]
    for frame_index in range(40):
        image = base((w, h), "01 / THE WORK", "AI · SYSTEMS · PEOPLE", color=(40, 82, 255))
        d = ImageDraw.Draw(image)
        d.text((38, 82), "IDEAS", font=font(78, True, impact=True), fill=NAVY)
        d.text((38, 158), "INTO", font=font(78, True, impact=True), fill=INK)
        d.text((38, 234), "SYSTEMS.", font=font(78, True, impact=True), fill=NAVY)
        d.text((42, 342), "HEALTH / AGRICULTURE / PUBLIC SYSTEMS", font=font(11, mono=True, bold=True), fill=NAVY)
        d.line((462, 72, 462, 300), fill=(115, 151, 255), width=2)
        d.text((510, 76), "HOW I BUILD", font=font(12, mono=True, bold=True), fill=ICE)
        phase = frame_index / 40 * tau
        for idx, (name, note) in enumerate(stages):
            y = 108 + idx * 49
            strength = (sin(phase + idx * 1.71) + 1) / 2
            fill = tuple(round(a + (b - a) * strength) for a, b in zip((20, 51, 192), (9, 16, 34)))
            edge = tuple(round(a + (b - a) * strength) for a, b in zip((113, 154, 255), ICE))
            d.rounded_rectangle((506, y, 1158, y + 40), radius=2, fill=fill, outline=edge, width=1)
            d.rectangle((506, y, 511, y + 40), fill=edge)
            d.text((530, y + 10), f"0{idx + 1}", font=font(12, mono=True, bold=True), fill=ICE)
            d.text((582, y + 7), name, font=font(18, True, mono=True), fill=INK)
            d.text((808, y + 11), note, font=font(12, mono=True), fill=ICE)
        d.text((510, 325), "HKBK · INFORMATION SCIENCE ENGINEERING", font=font(11, mono=True), fill=INK)
        d.text((1158, 345), "GOOGLE STUDENT AMBASSADOR", font=font(10, mono=True), fill=NAVY, anchor="ra")
        frames.append(image)
    save_gif("about", frames, duration=110)


def marquee_strip(tokens, fnt, foreground=INK, separator=BLUE_LIGHT, pad=50):
    measurer = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    width = sum(measurer.textlength(word, font=fnt) for word in tokens) + (len(tokens) - 1) * pad
    strip = Image.new("RGB", (max(1, int(width)), 38), NAVY)
    d = ImageDraw.Draw(strip)
    x = 0
    for i, word in enumerate(tokens):
        d.text((x, 3), word, font=fnt, fill=foreground)
        x += int(d.textlength(word, font=fnt))
        if i < len(tokens) - 1:
            d.text((x + 12, 8), "/", font=font(fnt.size, True, mono=True), fill=separator)
            x += pad
    return strip


def stack_panel():
    w, h = 1200, 320
    rows = [
        ("LANGUAGES", ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "C++"]),
        ("APPLICATIONS", ["REACT", "NEXT.JS", "FASTAPI", "NODE.JS"]),
        ("AI / VISION", ["YOLOv8", "OPENCV", "GEMINI", "LSTM", "RAG"]),
        ("DATA / DELIVERY", ["POSTGRESQL", "MONGODB", "REDIS", "FIREBASE", "DOCKER", "KUBERNETES", "VERCEL", "GOOGLE CLOUD", "LINUX", "GIT"]),
    ]
    strips = [marquee_strip(items, font(17, True, mono=True), pad=54) for _, items in rows]
    speeds = [3, -4, 5, -3]
    frames = []
    for frame_index in range(64):
        image = base((w, h), "02 / SELECTED TOOLKIT", "VERIFIED IN PROJECTS")
        d = ImageDraw.Draw(image)
        d.text((38, 51), "TOOLS THAT MOVE WORK.", font=font(39, True), fill=INK)
        d.text((40, 102), "Languages / product / applied AI / delivery", font=font(13, mono=True), fill=MUTED)
        for idx, ((label, _), strip, speed) in enumerate(zip(rows, strips, speeds)):
            y = 140 + idx * 43
            d.line((38, y - 5, 1162, y - 5), fill=LINE, width=1)
            d.text((42, y + 5), label, font=font(11, True, mono=True), fill=BLUE_LIGHT)
            x0, view_w, view_h = 250, 906, 34
            strip_width = strip.width
            direction = 1 if speed > 0 else -1
            offset = round(direction * frame_index * strip_width / 64) % strip_width
            lane = Image.new("RGB", (view_w, view_h), NAVY)
            left_w = min(view_w, strip_width - offset)
            lane.paste(strip.crop((offset, 0, offset + left_w, view_h)), (0, 0))
            if left_w < view_w:
                lane.paste(strip.crop((0, 0, view_w - left_w, view_h)), (left_w, 0))
            image.paste(lane, (x0, y))
        frames.append(image)
    save_gif("stack", frames, duration=70)


def project_panel():
    projects = ["AGRIVISION", "RAILSENSE AI", "EVIDENTIA", "QUEUEIQ", "CIPHER RANKER",
                "NAMMA KSP", "TARANG", "OPTIFRESH", "HEALTHLENS", "SPECFORGE"]
    w, h = 1200, 330
    frames = []
    cols, card_w, card_h, gap = 5, 214, 86, 12
    start_x, start_y = 38, 94
    for frame_index in range(36):
        image = base((w, h), "03 / SELECTED BUILDS", "REPOSITORIES · DEMOS LINKED BELOW")
        d = ImageDraw.Draw(image)
        d.text((38, 44), "PROJECT INDEX", font=font(42, True), fill=INK)
        d.text((1162, 62), "10 BUILDS", font=font(12, True, mono=True), fill=BLUE_LIGHT, anchor="ra")
        for idx, name in enumerate(projects):
            row, col = divmod(idx, cols)
            x = start_x + col * (card_w + gap)
            y = start_y + row * (card_h + 16)
            phase = frame_index / 36 * tau + idx * 0.83
            strength = (sin(phase) + 1) / 2
            mix = int(70 + 130 * strength)
            accent = (35, 75 + int(45 * strength), min(255, mix + 30))
            fill = tuple(int(a + (b - a) * (0.1 + 0.1 * strength)) for a, b in zip(PANEL, accent))
            d.rectangle((x, y, x + card_w, y + card_h), fill=fill, outline=LINE, width=1)
            d.rectangle((x, y, x + card_w, y + 4), fill=accent)
            d.text((x + 13, y + 12), f"{idx + 1:02}", font=font(11, True, mono=True), fill=BLUE_LIGHT)
            name_size = 21 if len(name) < 12 else 17
            d.text((x + 13, y + 36), name, font=font(name_size, True), fill=INK)
            arrow_x = x + card_w - 29 + round(9 * sin(phase + 0.7))
            d.text((arrow_x, y + 11), "↗", font=font(18, True), fill=ICE if strength > 0.52 else BLUE_LIGHT)
            if name in {"RAILSENSE AI", "QUEUEIQ", "CIPHER RANKER"}:
                d.text((x + card_w - 45, y + 59), "LIVE", font=font(9, True, mono=True), fill=ICE, anchor="ra")
        d.text((40, 297), "RESEARCH / PRODUCT / APPLIED AI", font=font(11, True, mono=True), fill=MUTED)
        d.text((1160, 297), "OPEN A BUILD ↗", font=font(11, True, mono=True), fill=BLUE_LIGHT, anchor="ra")
        frames.append(image)
    save_gif("projects", frames, duration=90)


def research_panel():
    w, h = 1200, 290
    cards = [("QUEUEIQ", "PAPER / MULTILINGUAL NLP", "READ PAPER"),
             ("AGRIVISION", "PAPER / PRECISION AGRICULTURE", "READ PAPER"),
             ("AROGYALENS", "HKBK TECHNOVATE / IEEE", "PRESENTED WORK")]
    frames = []
    for frame_index in range(36):
        image = base((w, h), "04 / RESEARCH & PUBLICATIONS", "PAPERS · PRESENTED WORK")
        d = ImageDraw.Draw(image)
        d.text((38, 50), "RESEARCH", font=font(43, True), fill=INK)
        d.text((42, 99), "PROTOTYPE → PAPER → PRACTICE", font=font(12, True, mono=True), fill=BLUE_LIGHT)
        x0, card_w, card_gap, y = 38, 356, 18, 136
        for idx, (title, detail, cta) in enumerate(cards):
            x = x0 + idx * (card_w + card_gap)
            phase = frame_index / 36 * tau + idx * 1.5
            glow = (sin(phase) + 1) / 2
            accent = tuple(round(a + (b - a) * (0.25 + 0.7 * glow)) for a, b in zip(BLUE, ICE))
            d.rectangle((x, y, x + card_w, 258), fill=PANEL, outline=LINE, width=1)
            d.rectangle((x, y, x + card_w, y + 4), fill=accent)
            d.text((x + 17, y + 17), f"0{idx + 1} / {('PAPER' if idx < 2 else 'SYMPOSIUM')}", font=font(10, True, mono=True), fill=BLUE_LIGHT)
            d.text((x + 17, y + 42), title, font=font(23, True), fill=INK)
            d.text((x + 17, y + 76), detail, font=font(10, mono=True), fill=MUTED)
            arrow_x = x + 20 + round(16 * (0.5 + 0.5 * sin(phase + 0.8)))
            d.text((arrow_x, y + 97), f"{cta}  ↗", font=font(12, True, mono=True), fill=accent)
        frames.append(image)
    save_gif("research", frames, duration=95)


def connect_panel():
    w, h = 1200, 230
    frames = []
    labels = ["LINKEDIN", "GITHUB / WORK", "PORTFOLIO", "EMAIL"]
    for frame_index in range(32):
        image = Image.new("RGB", (w, h), (243, 242, 234))
        d = ImageDraw.Draw(image)
        d.rectangle((0, 0, w, 7), fill=BLUE)
        d.text((38, 20), "05 / OPEN CHANNEL", font=font(12, True, mono=True), fill=BLUE)
        d.text((38, 62), "SAY", font=font(60, True, impact=True), fill=NAVY)
        d.text((38, 122), "HELLO.", font=font(60, True, impact=True), fill=BLUE)
        d.line((430, 48, 430, 204), fill=(195, 199, 205), width=1)
        for idx, label in enumerate(labels):
            y = 48 + idx * 38
            d.line((476, y, 1160, y), fill=(195, 199, 205), width=1)
            d.text((492, y + 10), f"0{idx + 1}", font=font(11, True, mono=True), fill=BLUE)
            d.text((540, y + 8), label, font=font(16, True, mono=True), fill=NAVY)
            phase = frame_index / 32 * tau + idx * 0.9
            x = 1128 + round(14 * sin(phase))
            d.line((x - 6, y + 17, x + 1, y + 17), fill=BLUE, width=3)
            d.line((x - 5, y + 12, x + 1, y + 17), fill=BLUE, width=3)
            d.line((x + 1, y + 17, x - 5, y + 22), fill=BLUE, width=3)
        d.line((476, 200, 1160, 200), fill=(195, 199, 205), width=1)
        frames.append(image)
    save_gif("connect", frames, duration=90)


def footer_panel():
    w, h = 1200, 130
    items = ["BUILD USEFUL THINGS", "AI / ML / SYSTEMS", "RESEARCH INTO REAL TOOLS", "SAMEER8549"]
    text_font = font(21, True, mono=True)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    run_w = int(sum(measure.textlength(s, font=text_font) for s in items) + 82 * len(items))
    run = Image.new("RGB", (run_w, 48), NAVY)
    rd = ImageDraw.Draw(run)
    x = 0
    for item in items:
        rd.text((x, 5), item, font=text_font, fill=INK)
        tw = int(rd.textlength(item, font=text_font))
        rd.rectangle((x, 42, x + tw, 46), fill=BLUE)
        x += tw + 82
    frames = []
    frame_count = 72
    for frame_index in range(frame_count):
        image = base((w, h), "06 / END TRANSMISSION", "KEEP BUILDING")
        d = ImageDraw.Draw(image)
        d.text((38, 47), "THANKS FOR THE SCROLL.", font=font(18, True), fill=BLUE_LIGHT)
        offset = round(frame_index * run_w / frame_count) % run_w
        lane = Image.new("RGB", (1124, 48), NAVY)
        left = min(1124, run_w - offset)
        lane.paste(run.crop((offset, 0, offset + left, 48)), (0, 0))
        if left < 1124:
            lane.paste(run.crop((0, 0, 1124 - left, 48)), (left, 0))
        image.paste(lane, (38, 74))
        frames.append(image)
    save_gif("footer", frames, duration=85)


def main():
    ASSETS.mkdir(exist_ok=True)
    animate_hero()
    about_panel()
    stack_panel()
    project_panel()
    research_panel()
    connect_panel()
    footer_panel()
    print("Rendered distinct looping hero, about, stack, project index, research, contact, and footer banners.")

if __name__ == "__main__":
    main()
