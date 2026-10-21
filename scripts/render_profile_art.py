#!/usr/bin/env python3
"""Render a coherent set of animated brutalist banners for the profile README."""

from math import cos, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# Palette sampled from the supplied banner reference: hard royal-blue paper,
# near-black ink, saturated navy panels, and small icy-white annotations.
ROYAL = (43, 82, 250)
ROYAL_DARK = (31, 60, 213)
NAVY = (8, 19, 68)
PANEL = (19, 43, 139)
PANEL_ALT = (25, 52, 162)
ICE = (244, 246, 255)
MUTED = (181, 198, 255)
LINE = (160, 183, 255)


def font(size, bold=False, mono=False, impact=False):
    if impact:
        options = ["C:/Windows/Fonts/impact.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"]
    elif mono:
        options = ["C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    else:
        options = ["C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for path in options:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def frame_base(size, kicker, right="SAMEER8549"):
    w, h = size
    im = Image.new("RGB", size, ROYAL)
    d = ImageDraw.Draw(im)
    d.text((38, 20), kicker, font=font(12, mono=True), fill=ICE)
    d.text((w - 38, 20), right, font=font(12, mono=True), fill=MUTED, anchor="ra")
    return im


def save(name, frames, duration=95):
    frames[0].save(ASSETS / f"{name}.gif", save_all=True, append_images=frames[1:],
                   duration=duration, loop=0, optimize=True, disposal=2)


def arrow(d, x, y, color, size=14, diagonal=False):
    width = max(2, size // 7)
    if diagonal:
        d.line((x, y + size, x + size, y), fill=color, width=width)
        d.line((x + size - size // 2, y, x + size, y, x + size, y + size // 2), fill=color, width=width)
    else:
        mid = y + size // 2
        d.line((x, mid, x + size, mid), fill=color, width=width)
        d.line((x + size // 2, y, x + size, mid, x + size // 2, y + size), fill=color, width=width)


def marquee(items, fnt, color=ICE, sep_color=MUTED, gap=66, height=46):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lengths = [int(probe.textlength(item, font=fnt)) for item in items]
    width = sum(lengths) + gap * len(items)
    strip = Image.new("RGB", (max(1, width), height), NAVY)
    d = ImageDraw.Draw(strip)
    x = 0
    for item, text_w in zip(items, lengths):
        d.text((x, 4), item, font=fnt, fill=color)
        x += text_w
        d.text((x + 16, 6), "/", font=font(fnt.size, True, mono=True), fill=sep_color)
        x += gap
    return strip


def clip_marquee(strip, width, height, offset):
    lane = Image.new("RGB", (width, height), NAVY)
    ox = offset % strip.width
    first = min(width, strip.width - ox)
    lane.paste(strip.crop((ox, 0, ox + first, height)), (0, 0))
    if first < width:
        lane.paste(strip.crop((0, 0, width - first, height)), (first, 0))
    return lane


def hero_panel():
    w, h, count = 1200, 430, 48
    portrait = Image.open(ASSETS / "sameer-portrait.png").convert("RGB")
    side = 288
    crop = min(portrait.width, portrait.height)
    left = (portrait.width - crop) // 2
    top = (portrait.height - crop) // 2
    portrait = portrait.crop((left, top, left + crop, top + crop)).resize((side, side), Image.Resampling.LANCZOS)
    ticker = marquee(["AI / ML", "FULL-STACK", "CREATIVE TECHNOLOGY", "BENGALURU, INDIA"], font(17, True, mono=True), gap=64, height=40)
    frames = []
    for i in range(count):
        im = frame_base((w, h), "SAMEER8549 / BUILDER PROFILE", "BENGALURU · INDIA")
        d = ImageDraw.Draw(im)
        d.text((38, 93), "ABDUL", font=font(100, True, impact=True), fill=NAVY)
        d.text((38, 185), "SAMEER", font=font(100, True, impact=True), fill=ICE)
        d.text((42, 307), "AI / ML ENGINEER", font=font(19, True, mono=True), fill=NAVY)
        d.text((42, 337), "FULL-STACK DEVELOPER", font=font(19, True, mono=True), fill=NAVY)
        # Portrait is framed like a printed cutout. A strong scan strip crosses
        # the picture once per loop; the moving ticker supplies continuous motion.
        x0, y0 = 810, 70
        d.rectangle((x0 - 13, y0 - 13, x0 + side + 13, y0 + side + 13), fill=NAVY)
        d.rectangle((x0 - 7, y0 - 7, x0 + side + 7, y0 + side + 7), outline=ICE, width=2)
        im.paste(portrait, (x0, y0))
        d.rectangle((x0 + 14, y0 + side + 24, x0 + side - 14, y0 + side + 55), fill=ICE)
        d.text((x0 + 25, y0 + side + 33), "AI / BUILDER", font=font(11, True, mono=True), fill=NAVY)
        im.paste(clip_marquee(ticker, 734, 40, i * ticker.width // count), (38, 379))
        frames.append(im)
    save("hero", frames, 80)


def about_panel():
    w, h, count = 1200, 370, 48
    rows = [("SEE", "VISION / SIGNAL"), ("REASON", "MODELS / CONTEXT"),
            ("CONNECT", "API / DATA"), ("SHIP", "PRODUCT / PEOPLE")]
    frames = []
    for i in range(count):
        im = frame_base((w, h), "01 / THE WORK", "AI · SYSTEMS · PEOPLE")
        d = ImageDraw.Draw(im)
        d.text((38, 82), "IDEAS", font=font(78, True, impact=True), fill=NAVY)
        d.text((38, 158), "INTO", font=font(78, True, impact=True), fill=ICE)
        d.text((38, 234), "SYSTEMS.", font=font(78, True, impact=True), fill=NAVY)
        d.text((42, 342), "HEALTH / AGRICULTURE / PUBLIC SYSTEMS", font=font(11, True, mono=True), fill=NAVY)
        d.line((462, 72, 462, 300), fill=LINE, width=2)
        d.text((510, 76), "HOW I BUILD", font=font(12, True, mono=True), fill=ICE)
        active = (i // (count // len(rows))) % len(rows)
        for idx, (title, sub) in enumerate(rows):
            y = 108 + idx * 49
            selected = idx == active
            fill = ICE if selected else PANEL
            text = NAVY if selected else ICE
            d.rectangle((506, y, 1158, y + 40), fill=fill, outline=ICE if selected else LINE, width=1)
            d.rectangle((506, y, 512, y + 40), fill=NAVY if selected else LINE)
            d.text((530, y + 10), f"0{idx + 1}", font=font(12, True, mono=True), fill=text)
            d.text((582, y + 7), title, font=font(18, True, mono=True), fill=text)
            d.text((808, y + 11), sub, font=font(12, mono=True), fill=text if selected else MUTED)
        d.text((510, 325), "HKBK · INFORMATION SCIENCE ENGINEERING", font=font(11, mono=True), fill=ICE)
        d.text((1158, 345), "GOOGLE STUDENT AMBASSADOR", font=font(10, True, mono=True), fill=NAVY, anchor="ra")
        frames.append(im)
    save("about", frames, 110)


def stack_panel():
    w, h, count = 1200, 330, 64
    rows = [
        ("LANGUAGES", ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "C++"]),
        ("APPLICATIONS", ["REACT", "NEXT.JS", "FASTAPI", "NODE.JS"]),
        ("AI / VISION", ["YOLOv8", "OPENCV", "GEMINI", "LSTM", "RAG"]),
        ("DATA / DELIVERY", ["POSTGRESQL", "MONGODB", "REDIS", "FIREBASE", "DOCKER", "KUBERNETES", "VERCEL", "GOOGLE CLOUD", "LINUX", "GIT"]),
    ]
    strips = [marquee(items * 2, font(16, True, mono=True), gap=60, height=34) for _, items in rows]
    speeds = [2, -3, 4, -2]
    frames = []
    for i in range(count):
        im = frame_base((w, h), "02 / SELECTED TOOLKIT", "VERIFIED IN PROJECTS")
        d = ImageDraw.Draw(im)
        d.text((38, 48), "TOOLS THAT MOVE WORK.", font=font(40, True, impact=True), fill=NAVY)
        d.text((40, 103), "LANGUAGES / PRODUCT / APPLIED AI / DELIVERY", font=font(12, True, mono=True), fill=ICE)
        for j, ((label, _), strip, speed) in enumerate(zip(rows, strips, speeds)):
            y = 139 + j * 43
            d.rectangle((38, y, 1162, y + 34), fill=PANEL if j % 2 == 0 else PANEL_ALT, outline=ICE, width=1)
            d.rectangle((38, y, 242, y + 34), fill=NAVY)
            d.text((50, y + 9), label, font=font(11, True, mono=True), fill=ICE)
            lane = clip_marquee(strip, 906, 34, i * speed)
            im.paste(lane, (256, y))
            d = ImageDraw.Draw(im)
        frames.append(im)
    save("stack", frames, 80)


def project_panel():
    w, h, count = 1200, 344, 64
    projects = ["AGRIVISION", "RAILSENSE AI", "EVIDENTIA", "QUEUEIQ", "CIPHER RANKER",
                "NAMMA KSP", "TARANG", "OPTIFRESH", "HEALTHLENS", "SPECFORGE"]
    card_w, card_h, gap = 214, 76, 13
    frames = []
    for i in range(count):
        im = frame_base((w, h), "03 / SELECTED BUILDS", "REPOSITORIES · DEMOS LINKED BELOW")
        d = ImageDraw.Draw(im)
        d.text((38, 47), "PROJECT INDEX", font=font(43, True, impact=True), fill=NAVY)
        d.text((1162, 62), "10 BUILDS", font=font(12, True, mono=True), fill=ICE, anchor="ra")
        for idx, name in enumerate(projects):
            row, col = divmod(idx, 5)
            x, y = 38 + col * (card_w + gap), 112 + row * 92
            d.rectangle((x, y, x + card_w, y + card_h), fill=PANEL if row == 0 else PANEL_ALT,
                        outline=ICE, width=1)
            d.rectangle((x, y, x + 5, y + card_h), fill=NAVY)
            d.text((x + 13, y + 12), f"{idx + 1:02}", font=font(10, True, mono=True), fill=MUTED)
            name_size = 19 if len(name) < 12 else 16
            d.text((x + 13, y + 35), name, font=font(name_size, True), fill=ICE)
            # The repository cue moves toward its target; titles stay fixed and readable.
            pulse = (1 - cos(i / count * tau)) / 2
            arrow_x = x + card_w - 33 + round(8 * pulse)
            arrow(d, arrow_x, y + 10, ICE, size=13, diagonal=True)
        d.text((40, 314), "RESEARCH / PRODUCT / APPLIED AI", font=font(11, True, mono=True), fill=NAVY)
        d.text((1117, 314), "OPEN A BUILD", font=font(11, True, mono=True), fill=NAVY, anchor="ra")
        arrow(d, 1133, 311, NAVY, size=11, diagonal=True)
        frames.append(im)
    save("projects", frames, 85)


def research_panel():
    w, h, count = 1200, 292, 48
    cards = [("QUEUEIQ", "MULTILINGUAL NLP", "READ PAPER"),
             ("AGRIVISION", "PRECISION AGRICULTURE", "READ PAPER"),
             ("AROGYALENS", "HKBK TECHNOVATE / IEEE", "PRESENTED WORK")]
    frames = []
    for i in range(count):
        im = frame_base((w, h), "04 / RESEARCH & PUBLICATIONS", "PAPERS · PRESENTED WORK")
        d = ImageDraw.Draw(im)
        d.text((38, 48), "RESEARCH", font=font(43, True, impact=True), fill=NAVY)
        d.text((42, 99), "PROTOTYPE / PAPER / PRACTICE", font=font(12, True, mono=True), fill=ICE)
        active = (i // 16) % 3
        for idx, (title, detail, cta) in enumerate(cards):
            x, y, cw, ch = 38 + idx * 376, 139, 356, 112
            focus = idx == active
            fill = ICE if focus else PANEL
            ink = NAVY if focus else ICE
            d.rectangle((x, y, x + cw, y + ch), fill=fill, outline=ICE, width=1)
            d.rectangle((x, y, x + cw, y + 5), fill=NAVY if focus else LINE)
            d.text((x + 17, y + 16), f"0{idx + 1} / {'PAPER' if idx < 2 else 'SYMPOSIUM'}", font=font(10, True, mono=True), fill=ink)
            d.text((x + 17, y + 39), title, font=font(23, True), fill=ink)
            d.text((x + 17, y + 72), detail, font=font(10, True, mono=True), fill=ink if focus else MUTED)
            d.text((x + 17, y + 91), cta, font=font(10, True, mono=True), fill=ink)
            cta_width = int(d.textlength(cta, font=font(10, True, mono=True)))
            arrow(d, x + 21 + cta_width, y + 90, ink, size=10, diagonal=True)
            if focus:
                sweep = x + 6 + (i % 16) * (cw - 12) // 16
                d.rectangle((sweep, y + 5, sweep + 5, y + ch - 1), fill=ROYAL)
        frames.append(im)
    save("research", frames, 105)


def connect_panel():
    w, h, count = 1200, 248, 40
    links = ["LINKEDIN", "GITHUB / WORK", "PORTFOLIO", "EMAIL"]
    frames = []
    for i in range(count):
        im = frame_base((w, h), "05 / OPEN CHANNEL", "CONNECT · COLLABORATE · BUILD")
        d = ImageDraw.Draw(im)
        d.text((38, 83), "SAY", font=font(68, True, impact=True), fill=NAVY)
        d.text((38, 151), "HELLO.", font=font(68, True, impact=True), fill=ICE)
        d.line((430, 56, 430, 219), fill=LINE, width=2)
        active = (i // 10) % 4
        for idx, label in enumerate(links):
            y = 57 + idx * 40
            selected = idx == active
            d.rectangle((476, y, 1162, y + 34), fill=ICE if selected else PANEL, outline=ICE, width=1)
            ink = NAVY if selected else ICE
            d.text((495, y + 9), f"0{idx + 1}", font=font(11, True, mono=True), fill=ink)
            d.text((545, y + 8), label, font=font(15, True, mono=True), fill=ink)
            shift = 8 + (i % 10) * 2
            ax = 1123 + shift
            arrow(d, ax, y + 11, ink, size=14)
        frames.append(im)
    save("connect", frames, 100)


def footer_panel():
    w, h, count = 1200, 146, 72
    items = ["BUILD USEFUL THINGS", "AI / ML / SYSTEMS", "RESEARCH INTO REAL TOOLS", "SAMEER8549"]
    strip = marquee(items * 2, font(24, True, mono=True), gap=82, height=56)
    frames = []
    for i in range(count):
        im = frame_base((w, h), "06 / END TRANSMISSION", "KEEP BUILDING")
        d = ImageDraw.Draw(im)
        d.text((38, 48), "THANKS FOR THE SCROLL.", font=font(17, True, mono=True), fill=NAVY)
        im.paste(clip_marquee(strip, 1124, 56, i * strip.width // count), (38, 76))
        d = ImageDraw.Draw(im)
        d.rectangle((38, 137, 1162, 140), fill=NAVY)
        frames.append(im)
    save("footer", frames, 80)


def main():
    ASSETS.mkdir(exist_ok=True)
    hero_panel()
    about_panel()
    stack_panel()
    project_panel()
    research_panel()
    connect_panel()
    footer_panel()
    print("Rendered seven autoplaying royal-blue README banners.")


if __name__ == "__main__":
    main()
