#!/usr/bin/env python3
"""Render the animated, panel-only art used by the GitHub profile README."""

from math import cos, pi
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROJECTS_DIR = ASSETS / "projects"
RESEARCH_DIR = ASSETS / "research"

ROYAL = (43, 82, 250)
BLUE = (62, 116, 255)
NAVY = (8, 19, 68)
PANEL = (19, 43, 139)
PANEL_ALT = (25, 52, 162)
ICE = (244, 246, 255)
MUTED = (181, 198, 255)
LINE = (160, 183, 255)
GRID = (48, 80, 224)

PROJECTS = [
    ("agrivision", "AGRIVISION", "PRECISION FARMING", "AI / COMPUTER VISION"),
    ("railsense", "RAILSENSE AI", "RAIL OPERATIONS", "PASSENGER + STAFF TOOLS"),
    ("evidentia", "EVIDENTIA", "EVIDENCE VERIFICATION", "REPRODUCIBLE RECEIPTS"),
    ("queueiq", "QUEUEIQ", "HOSPITAL FLOW", "MULTILINGUAL NLP"),
    ("cipher-ranker", "CIPHER RANKER", "CANDIDATE RANKING", "EVIDENCE-BOUND AI"),
    ("namma-ksp", "NAMMA KSP", "CIVIC INTELLIGENCE", "SYNTHETIC FIR DATA"),
    ("tarang", "TARANG", "MARITIME RESCUE", "PUBLIC SAFETY SYSTEMS"),
    ("optifresh", "OPTIFRESH", "FOOD FRESHNESS", "COMPUTER VISION"),
    ("healthlens", "HEALTHLENS", "AI HEALTH CHECK", "HEALTH TECHNOLOGY"),
    ("specforge", "SPECFORGE", "STRUCTURED PRODUCT DATA", "PRODUCT INTELLIGENCE"),
]


def font(size, bold=False, mono=False, display=False):
    if display:
        paths = ["C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    elif mono:
        paths = ["C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf"]
    else:
        paths = ["C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def base(size, left, right="SAMEER8549"):
    w, h = size
    im = Image.new("RGB", size, ROYAL)
    d = ImageDraw.Draw(im)
    # Fine registration grid: visible at full size, quiet behind the panels.
    for x in range(20, w, 40):
        d.line((x, 0, x, h), fill=GRID, width=1)
    for y in range(20, h, 40):
        d.line((0, y, w, y), fill=GRID, width=1)
    d.rectangle((0, 0, w, 38), fill=NAVY)
    d.text((26, 12), left, font=font(11, True, mono=True), fill=ICE)
    d.text((w - 26, 12), right, font=font(11, True, mono=True), fill=MUTED, anchor="ra")
    return im


def save_gif(path, frames, duration):
    path.parent.mkdir(parents=True, exist_ok=True)
    palette = frames[0].convert("P", palette=Image.Palette.ADAPTIVE, colors=160)
    quantized = [frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
                 for frame in frames]
    quantized[0].save(path, save_all=True, append_images=quantized[1:],
                      duration=duration, loop=0, optimize=True, disposal=2)


def make_strip(items, fnt, height, gap=42):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    cycle = sum(int(probe.textlength(s, font=fnt)) + gap for s in items)
    strip = Image.new("RGB", (cycle * 2, height), NAVY)
    d = ImageDraw.Draw(strip)
    for pass_index in range(2):
        x = pass_index * cycle
        for item in items:
            width = int(d.textlength(item, font=fnt))
            d.text((x, (height - fnt.size) // 2 - 1), item, font=fnt, fill=ICE)
            x += width
            d.text((x + 13, (height - fnt.size) // 2 - 1), "/", font=font(fnt.size, True, mono=True), fill=MUTED)
            x += gap
    return strip, cycle


def paste_strip(im, strip, cycle, box, offset):
    x, y, w, h = box
    start = offset % cycle
    first = min(w, strip.width - start)
    im.paste(strip.crop((start, 0, start + first, h)), (x, y))
    if first < w:
        im.paste(strip.crop((0, 0, w - first, h)), (x + first, y))


def portrait_circle(side):
    image = Image.open(ASSETS / "sameer-portrait.png").convert("RGB")
    image = image.resize((side, side), Image.Resampling.LANCZOS).convert("RGBA")
    scale = 4
    mask = Image.new("L", (side * scale, side * scale), 0)
    ImageDraw.Draw(mask).ellipse((3 * scale, 3 * scale, (side - 3) * scale, (side - 3) * scale), fill=255)
    image.putalpha(mask.resize((side, side), Image.Resampling.LANCZOS))
    return image


def hero_panel():
    w, h, count = 1200, 365, 48
    avatar_side = 244
    avatar = portrait_circle(avatar_side)
    ticker, cycle = make_strip(["AI / ML ENGINEER", "FULL-STACK DEVELOPER", "CREATIVE TECHNOLOGY"],
                              font(15, True, mono=True), 36, 50)
    frames = []
    for i in range(count):
        im = base((w, h), "SAMEER8549 / BUILDER PROFILE", "BENGALURU / INDIA")
        d = ImageDraw.Draw(im)
        d.rectangle((36, 58, 790, 304), fill=ROYAL)
        d.rectangle((36, 58, 790, 304), outline=ICE, width=1)
        d.rectangle((36, 58, 49, 304), fill=NAVY)
        d.text((72, 78), "ABDUL", font=font(82, True, display=True), fill=NAVY)
        d.text((72, 153), "SAMEER", font=font(82, True, display=True), fill=ICE)
        d.text((77, 255), "AI / ML  ·  FULL-STACK", font=font(16, True, mono=True), fill=NAVY)
        d.rectangle((824, 52, 1146, 328), fill=NAVY, outline=ICE, width=1)
        d.rectangle((837, 65, 1111, 339), fill=PANEL)
        im.paste(avatar, (852, 78), avatar)
        d = ImageDraw.Draw(im)
        d.rectangle((72, 312, 790, 348), fill=NAVY)
        paste_strip(im, ticker, cycle, (86, 312, 690, 36), int(i * cycle / count))
        d = ImageDraw.Draw(im)
        d.text((1129, 345), "01 / 08", font=font(10, True, mono=True), fill=ICE, anchor="ra")
        # A slow underline pulse supplies motion without scanning across the portrait.
        span = 118
        px = 72 + int((1 - cos((i / count) * 2 * pi)) * 0.5 * (670 - span))
        d.rectangle((72, 352, 742, 355), fill=PANEL)
        d.rectangle((px, 352, px + span, 355), fill=ICE)
        frames.append(im)
    save_gif(ASSETS / "hero.gif", frames, 180)


def about_panel():
    w, h, count = 1200, 310, 48
    rows = [("01", "SEE", "VISION / SIGNAL"), ("02", "REASON", "MODELS / CONTEXT"),
            ("03", "CONNECT", "API / DATA"), ("04", "SHIP", "PRODUCT / PEOPLE")]
    frames = []
    for i in range(count):
        im = base((w, h), "01 / THE WORK", "AI / SYSTEMS / PEOPLE")
        d = ImageDraw.Draw(im)
        d.text((40, 58), "IDEAS", font=font(75, True, display=True), fill=NAVY)
        d.text((40, 126), "INTO", font=font(75, True, display=True), fill=ICE)
        d.text((40, 194), "SYSTEMS.", font=font(75, True, display=True), fill=NAVY)
        d.text((45, 279), "HEALTH / AGRICULTURE / RAIL / CIVIC", font=font(11, True, mono=True), fill=ICE)
        d.line((432, 57, 432, 270), fill=LINE, width=2)
        d.text((474, 63), "HOW I BUILD", font=font(12, True, mono=True), fill=ICE)
        active = (i // 12) % len(rows)
        for idx, (number, label, detail) in enumerate(rows):
            y = 89 + idx * 47
            focus = idx == active
            fill = ICE if focus else PANEL
            ink = NAVY if focus else ICE
            d.rectangle((470, y, 1156, y + 38), fill=fill, outline=ICE if focus else LINE, width=1)
            d.rectangle((470, y, 476, y + 38), fill=NAVY if focus else LINE)
            d.text((492, y + 10), number, font=font(11, True, mono=True), fill=ink)
            d.text((545, y + 7), label, font=font(17, True, mono=True), fill=ink)
            d.text((784, y + 11), detail, font=font(11, True, mono=True), fill=ink if focus else MUTED)
        d.text((475, 286), "HKBK / INFORMATION SCIENCE ENGINEERING", font=font(10, True, mono=True), fill=ICE)
        d.text((1155, 286), "GOOGLE STUDENT AMBASSADOR", font=font(10, True, mono=True), fill=ICE, anchor="ra")
        frames.append(im)
    save_gif(ASSETS / "about.gif", frames, 180)


def stack_panel():
    w, h, count = 1200, 338, 72
    rows = [
        ("LANGUAGES", ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "C++"]),
        ("APPLICATIONS", ["REACT", "NEXT.JS", "FASTAPI", "NODE.JS"]),
        ("AI / VISION", ["YOLOv8", "OPENCV", "GEMINI", "LSTM", "RAG"]),
        ("DATA / DELIVERY", ["POSTGRESQL", "MONGODB", "REDIS", "FIREBASE", "DOCKER", "KUBERNETES", "VERCEL", "GOOGLE CLOUD", "LINUX", "GIT"]),
    ]
    strips = [make_strip(items, font(14, True, mono=True), 34, 47) for _, items in rows]
    frames = []
    for i in range(count):
        im = base((w, h), "02 / SELECTED TOOLKIT", "VERIFIED IN PROJECTS")
        d = ImageDraw.Draw(im)
        d.text((38, 50), "TOOLS IN THE BUILD.", font=font(40, True, display=True), fill=NAVY)
        d.text((42, 96), "LANGUAGE / PRODUCT / APPLIED AI / DELIVERY", font=font(11, True, mono=True), fill=ICE)
        for idx, ((label, _), (strip, cycle)) in enumerate(zip(rows, strips)):
            y = 132 + idx * 47
            d.rectangle((38, y, 1162, y + 34), fill=PANEL if idx % 2 == 0 else PANEL_ALT, outline=ICE, width=1)
            d.rectangle((38, y, 246, y + 34), fill=NAVY)
            d.text((51, y + 10), label, font=font(10, True, mono=True), fill=ICE)
            # The content drift is one full cycle per 10.8-second loop.
            offset = int(i * cycle / count)
            paste_strip(im, strip, cycle, (260, y, 894, 34), offset)
            d = ImageDraw.Draw(im)
        d.text((40, 326), "CLICKABLE TECHNOLOGY MARKS BELOW", font=font(10, True, mono=True), fill=ICE)
        d.text((1160, 326), "ROYAL BLUE / BUILDER STACK", font=font(10, True, mono=True), fill=ICE, anchor="ra")
        frames.append(im)
    save_gif(ASSETS / "stack.gif", frames, 150)


def index_panel(name, kicker, title, right, total="10", width=1200, height=116):
    count = 48
    frames = []
    for i in range(count):
        im = base((width, height), kicker, right)
        d = ImageDraw.Draw(im)
        d.rectangle((28, 48, width - 28, 100), fill=PANEL, outline=ICE, width=1)
        d.rectangle((28, 48, 39, 100), fill=NAVY)
        d.text((56, 52), title, font=font(36, True, display=True), fill=ICE)
        d.text((width - 52, 69), f"01 / {total}", font=font(11, True, mono=True), fill=MUTED, anchor="ra")
        x = 48 + int(i * (width - 96) / count)
        d.rectangle((x, 96, min(width - 48, x + 76), 100), fill=ICE)
        frames.append(im)
    save_gif(ASSETS / name, frames, 180)


def card_gif(path, index, name, detail, category, kicker="SELECTED BUILD"):
    w, h, count = 560, 146, 30
    frames = []
    for i in range(count):
        im = base((w, h), f"{kicker} / {index:02}", "OPEN REPOSITORY")
        d = ImageDraw.Draw(im)
        d.rectangle((18, 48, 542, 132), fill=PANEL if index % 2 else PANEL_ALT, outline=ICE, width=1)
        d.rectangle((18, 48, 29, 132), fill=NAVY)
        d.text((48, 56), f"{index:02}", font=font(11, True, mono=True), fill=MUTED)
        title_size = 26 if len(name) <= 14 else 21
        d.text((86, 53), name, font=font(title_size, True), fill=ICE)
        d.text((49, 91), detail, font=font(11, True, mono=True), fill=ICE)
        d.text((49, 112), category, font=font(9, True, mono=True), fill=MUTED)
        # A measured edge signal moves along the bottom rail, then rests.
        rail_x = 48 + int(i * 448 / count)
        d.rectangle((48, 127, 512, 130), fill=NAVY)
        d.rectangle((rail_x, 127, min(rail_x + 46, 512), 130), fill=ICE)
        # Small arrow shifts only two pixels over the whole loop.
        shift = round(2 * (1 - cos(2 * pi * i / count)) / 2)
        d.line((505 + shift, 66, 520 + shift, 66), fill=ICE, width=2)
        d.line((514 + shift, 60, 520 + shift, 66, 514 + shift, 72), fill=ICE, width=2)
        frames.append(im)
    save_gif(path, frames, 300)


def research_card(path, index, title, detail, url_label):
    w, h, count = 560, 156, 32
    frames = []
    for i in range(count):
        im = base((w, h), f"RESEARCH / {index:02}", "PAPER LINKED")
        d = ImageDraw.Draw(im)
        d.rectangle((18, 48, 542, 142), fill=PANEL, outline=ICE, width=1)
        d.rectangle((18, 48, 29, 142), fill=NAVY)
        d.text((48, 56), title, font=font(25, True), fill=ICE)
        d.text((49, 91), detail, font=font(10, True, mono=True), fill=MUTED)
        d.text((49, 116), url_label, font=font(10, True, mono=True), fill=ICE)
        x = 48 + int(i * 450 / count)
        d.rectangle((48, 136, 512, 139), fill=NAVY)
        d.rectangle((x, 136, min(x + 42, 512), 139), fill=ICE)
        frames.append(im)
    save_gif(path, frames, 300)


def activity_panel():
    """Animate only the light around fixed cells; the dated contribution data stays fixed."""
    from generate_activity import render_frames
    save_gif(ASSETS / "activity.gif", render_frames(), 240)


def connect_panel():
    w, h, count = 1200, 190, 48
    links = ["LINKEDIN", "GITHUB", "PORTFOLIO", "EMAIL"]
    frames = []
    for i in range(count):
        im = base((w, h), "07 / OPEN CHANNEL", "CONNECT / COLLABORATE / BUILD")
        d = ImageDraw.Draw(im)
        d.text((38, 65), "SAY", font=font(62, True, display=True), fill=NAVY)
        d.text((38, 119), "HELLO.", font=font(62, True, display=True), fill=ICE)
        d.line((354, 51, 354, 164), fill=LINE, width=2)
        active = (i // 12) % 4
        for idx, label in enumerate(links):
            x = 390 + idx * 193
            selected = idx == active
            fill, ink = (ICE, NAVY) if selected else (PANEL, ICE)
            d.rectangle((x, 75, x + 178, 129), fill=fill, outline=ICE, width=1)
            d.text((x + 14, 82), f"0{idx + 1}", font=font(10, True, mono=True), fill=ink)
            d.text((x + 14, 100), label, font=font(14, True, mono=True), fill=ink)
            d.line((x + 148, 103, x + 162, 103), fill=ink, width=2)
            d.line((x + 156, 97, x + 162, 103, x + 156, 109), fill=ink, width=2)
        frames.append(im)
    save_gif(ASSETS / "connect.gif", frames, 200)


def footer_panel():
    w, h, count = 1200, 108, 48
    strip, cycle = make_strip(["BUILD USEFUL THINGS", "AI / ML / SYSTEMS", "RESEARCH INTO TOOLS"],
                              font(19, True, mono=True), 42, 48)
    frames = []
    for i in range(count):
        im = base((w, h), "08 / END TRANSMISSION", "KEEP BUILDING")
        d = ImageDraw.Draw(im)
        d.rectangle((28, 47, 1172, 97), fill=NAVY, outline=ICE, width=1)
        paste_strip(im, strip, cycle, (42, 51, 1095, 42), int(i * cycle / count))
        d = ImageDraw.Draw(im)
        d.rectangle((28, 102, 1172, 105), fill=PANEL)
        x = 28 + int(i * 1144 / count)
        d.rectangle((x, 102, min(96 + x, 1172), 105), fill=ICE)
        frames.append(im)
    save_gif(ASSETS / "footer.gif", frames, 200)


def live_badge():
    w, h, count = 144, 42, 24
    frames = []
    for i in range(count):
        im = Image.new("RGB", (w, h), PANEL)
        d = ImageDraw.Draw(im)
        d.rectangle((1, 1, w - 2, h - 2), outline=ICE, width=1)
        d.ellipse((12, 14, 22, 24), fill=ICE)
        d.text((31, 11), "LIVE / DEMO", font=font(11, True, mono=True), fill=ICE)
        x = 8 + int(i * (w - 32) / count)
        d.rectangle((8, 34, w - 8, 37), fill=NAVY)
        d.rectangle((x, 34, min(x + 20, w - 8), 37), fill=ICE)
        frames.append(im)
    save_gif(ASSETS / "live-badge.gif", frames, 300)


def main():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    hero_panel()
    about_panel()
    stack_panel()
    index_panel("projects-index.gif", "03 / FIELD NOTES", "PROJECT INDEX", "10 SELECTED BUILDS")
    for index, (slug, name, detail, category) in enumerate(PROJECTS, start=1):
        card_gif(PROJECTS_DIR / f"{slug}.gif", index, name, detail, category)
    index_panel("research-index.gif", "04 / RESEARCH", "PAPERS IN PRACTICE", "2 VERIFIED PAPERS", total="02")
    research_card(RESEARCH_DIR / "queueiq.gif", 1, "QUEUEIQ", "MULTILINGUAL HOSPITAL QUEUE INTELLIGENCE", "DOI / 10.5281/ZENODO.20251618")
    research_card(RESEARCH_DIR / "agrivision.gif", 2, "AGRIVISION", "DEEP LEARNING / IOT / DRONE REMOTE SENSING", "ACADEMIA.EDU / PAPER")
    activity_panel()
    connect_panel()
    footer_panel()
    live_badge()
    print("Rendered slow-loop royal-blue README panels and linked-card art.")


if __name__ == "__main__":
    main()
