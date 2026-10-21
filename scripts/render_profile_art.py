#!/usr/bin/env python3
"""Render the compact, coordinated motion panels used by README.md."""

from math import sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = (7, 11, 20)
PANEL = (13, 19, 33)
LINE = (42, 55, 78)
BLUE = (48, 103, 255)
ICE = (157, 201, 255)
INK = (242, 245, 250)
MUTED = (133, 151, 181)


def font(size, bold=False, mono=False):
    if mono:
        options = ["C:/Windows/Fonts/consola.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
    else:
        options = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for option in options:
        if Path(option).exists():
            return ImageFont.truetype(option, size)
    return ImageFont.load_default()


def frame_base(size, label, right_label):
    im = Image.new("RGB", size, NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, size[0], 6), fill=BLUE)
    for x in range(0, size[0], 32):
        d.line((x, 6, x, size[1]), fill=(12, 18, 31), width=1)
    for y in range(6, size[1], 32):
        d.line((0, y, size[0], y), fill=(12, 18, 31), width=1)
    d.text((38, 20), label, font=font(12, mono=True), fill=ICE)
    d.text((size[0] - 38, 20), right_label, font=font(12, mono=True), fill=MUTED, anchor="ra")
    return im


def save_gif(name, frames, duration=120):
    frames[0].save(ASSETS / f"{name}.gif", save_all=True,
                   append_images=frames[1:], duration=duration,
                   loop=0, optimize=True, disposal=2)


def about_panel():
    im = frame_base((1200, 178), "01 / BUILDING GROUND", "BENGALURU · INDIA")
    d = ImageDraw.Draw(im)
    d.text((38, 54), "HUMAN", font=font(48, True), fill=INK)
    d.text((38, 101), "SYSTEMS.", font=font(48, True), fill=BLUE)
    d.text((42, 154), "HKBK / INFORMATION SCIENCE ENGINEERING", font=font(11, mono=True), fill=MUTED)
    d.line((424, 50, 424, 150), fill=LINE, width=2)
    d.text((468, 57), "THE WORK", font=font(12, mono=True), fill=ICE)
    topics = [(468, "HEALTH"), (690, "AGRICULTURE"), (950, "PUBLIC SYSTEMS")]
    for x, label in topics:
        d.rectangle((x, 88, x + 184, 134), fill=PANEL, outline=LINE, width=1)
        d.rectangle((x, 88, x + 4, 134), fill=BLUE)
        d.text((x + 15, 104), label, font=font(13, mono=True), fill=INK)
    d.text((468, 151), "GOOGLE STUDENT AMBASSADOR", font=font(11, mono=True), fill=MUTED)
    return im


def stack_panels():
    w, h = 1200, 206
    base = frame_base((w, h), "02 / SELECTED TOOLKIT", "VERIFIED IN PROJECTS")
    d = ImageDraw.Draw(base)
    d.text((38, 54), "TOOLS I BUILD WITH.", font=font(42, True), fill=INK)
    d.text((40, 105), "LANGUAGE / MODEL / PRODUCT / DELIVERY", font=font(12, mono=True), fill=MUTED)
    d.line((38, 132, w - 38, 132), fill=LINE, width=1)
    items = ["PYTHON", "JAVASCRIPT", "TYPESCRIPT", "REACT", "NEXT.JS", "FASTAPI", "NODE.JS", "YOLOv8", "OPENCV", "GEMINI", "POSTGRESQL", "MONGODB", "REDIS", "FIREBASE", "DOCKER", "KUBERNETES", "VERCEL", "GOOGLE CLOUD", "LINUX", "GIT"]
    item_font = font(13, mono=True)
    widths = [int(d.textlength(name, font=item_font)) + 35 for name in items]
    gap = 15
    tile_width = sum(widths) + gap * len(items)
    frames = []
    count = 80
    for i in range(count):
        image = base.copy()
        draw = ImageDraw.Draw(image)
        offset = round(tile_width * i / count)
        x0 = -offset
        while x0 < w:
            x = x0
            for idx, name in enumerate(items):
                box_w = widths[idx]
                draw.rectangle((x, 151, x + box_w, 188), fill=PANEL, outline=LINE, width=1)
                draw.rectangle((x, 151, x + 3, 188), fill=BLUE)
                draw.text((x + 13, 163), name, font=item_font, fill=INK)
                x += box_w + gap
            x0 += tile_width
        frames.append(image)
    return frames


def research_panels():
    w, h = 1200, 178
    base = frame_base((w, h), "03 / RESEARCH", "PAPERS · PRESENTED WORK")
    d = ImageDraw.Draw(base)
    d.text((38, 58), "PUBLISHED", font=font(38, True), fill=INK)
    d.text((38, 103), "+ PRESENTED.", font=font(38, True), fill=BLUE)
    d.line((410, 52, 410, 151), fill=LINE, width=2)
    cards = [(454, "QUEUEIQ", "PAPER / MULTILINGUAL NLP"),
             (704, "AGRIVISION", "PAPER / PRECISION AGRICULTURE"),
             (954, "AROGYALENS", "HKBK TECHNOVATE / 2026")]
    for x, title, subtitle in cards:
        d.rectangle((x, 56, x + 210, 142), fill=PANEL, outline=LINE, width=1)
        d.rectangle((x, 56, x + 210, 59), fill=BLUE)
        d.text((x + 14, 77), title, font=font(16, True), fill=INK)
        d.text((x + 14, 111), subtitle, font=font(9, mono=True), fill=MUTED)
    return base, [(664, 56), (914, 56), (1164, 56)]


def connect_panels():
    w, h = 1200, 184
    base = frame_base((w, h), "04 / OPEN CHANNEL", "LINKS BELOW")
    d = ImageDraw.Draw(base)
    d.text((38, 57), "SAY", font=font(52, True), fill=INK)
    d.text((38, 109), "HELLO.", font=font(52, True), fill=BLUE)
    d.line((424, 52, 424, 154), fill=LINE, width=2)
    labels = ["LINKEDIN", "GITHUB / WORK", "PORTFOLIO", "EMAIL"]
    rows = []
    for idx, label in enumerate(labels):
        y = 46 + idx * 32
        d.line((474, y, 1158, y), fill=LINE, width=1)
        d.text((490, y + 8), f"0{idx + 1}", font=font(10, mono=True), fill=BLUE)
        d.text((536, y + 6), label, font=font(14, True, mono=True), fill=INK)
        rows.append((1142, y + 15))
    d.line((474, 174, 1158, 174), fill=LINE, width=1)
    frames = []
    for i in range(24):
        image = base.copy()
        draw = ImageDraw.Draw(image)
        for idx, (x0, y0) in enumerate(rows):
            x = x0 + round(4 * sin(i / 24 * tau + idx * 1.2))
            draw.line((x - 4, y0 - 4, x, y0), fill=ICE, width=2)
            draw.line((x, y0, x - 4, y0 + 4), fill=ICE, width=2)
        frames.append(image)
    return frames


def animate_research(base, points):
    frames = []
    for i in range(24):
        phase = i / 24 * tau
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)
        for idx, (x, y) in enumerate(points):
            strength = 0.25 + 0.75 * (0.5 + 0.5 * sin(phase + idx * 1.6))
            draw.rectangle((x - 5, y - 5, x + 5, y + 5), fill=(*ICE, int(180 * strength)))
        bloom = glow.filter(ImageFilter.GaussianBlur(6))
        frame = base.convert("RGBA")
        frame.alpha_composite(bloom)
        frame.alpha_composite(glow)
        frames.append(frame.convert("RGB"))
    return frames


def main():
    ASSETS.mkdir(exist_ok=True)
    about_panel().save(ASSETS / "about.gif", save_all=False)
    save_gif("stack", stack_panels(), duration=100)
    research_base, points = research_panels()
    save_gif("research", animate_research(research_base, points), duration=120)
    save_gif("connect", connect_panels(), duration=120)
    print("Rendered compact intro, moving toolkit ticker, research panel, and contact panel.")


if __name__ == "__main__":
    main()
