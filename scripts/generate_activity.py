#!/usr/bin/env python3
"""Fetch and animate Sameer8549's real rolling-year GitHub contribution calendar."""

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import math
import re
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont

USERNAME = "Sameer8549"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "activity.gif"
WIDTH, HEIGHT = 1200, 340
BG = (7, 10, 17)
INK = (242, 242, 236)
MUTED = (153, 169, 205)
BLUE = (39, 82, 255)
LEVELS = [(18, 26, 44), (20, 48, 103), (25, 73, 161), (35, 105, 220), (91, 169, 255)]

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
    def handle_starttag(self, tag, attrs):
        if tag != "td":
            return
        values = dict(attrs)
        day, level = values.get("data-date"), values.get("data-level")
        if day and level is not None:
            self.cells[date.fromisoformat(day)] = int(level)

def fetch_calendar():
    url = f"https://github.com/users/{USERNAME}/contributions"
    request = urllib.request.Request(url, headers={"User-Agent": "Sameer8549-profile-activity/3.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    match = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    if not match:
        raise RuntimeError("GitHub contribution heading was not found")
    heading = " ".join(re.sub(r"<[^>]+>", " ", match.group(1)).split())
    total_match = re.search(r"([\d,]+)\s+contributions?\s+in the last year", heading, re.I)
    if not total_match:
        raise RuntimeError(f"Unexpected GitHub contribution heading: {heading!r}")
    parser = CalendarParser()
    parser.feed(html)
    if not parser.cells:
        raise RuntimeError("GitHub contribution cells were not found")
    return int(total_match.group(1).replace(",", "")), parser.cells

def font(size, bold=False):
    options = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for option in options:
        if option.exists():
            return ImageFont.truetype(str(option), size)
    return ImageFont.load_default()

def render(total, contributions):
    start, end = min(contributions), max(contributions)
    first_sunday = start.toordinal() - ((start.weekday() + 1) % 7)
    week_count = math.ceil((end.toordinal() - first_sunday + 1) / 7)
    cols, rows, cell, gap = week_count, 7, 14, 5
    stride = cell + gap
    grid_w = cols * cell + (cols - 1) * gap
    grid_x, grid_y = (WIDTH - grid_w) // 2, 188
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 7), fill=BLUE)
    draw.text((42, 25), f"{total:,}", font=font(54, True), fill=INK)
    draw.text((45, 89), "CONTRIBUTIONS / LAST 12 MONTHS", font=font(14, True), fill=BLUE)
    draw.text((1158, 34), "LIVE FIELD RECORD", font=font(14, True), fill=MUTED, anchor="ra")
    draw.text((1158, 61), f"{start:%d %b %Y} — {end:%d %b %Y}", font=font(16), fill=INK, anchor="ra")
    draw.line((42, 125, 1158, 125), fill=(51, 65, 99), width=1)
    draw.text((42, 143), "PUBLIC GITHUB ACTIVITY", font=font(11, True), fill=MUTED)

    # Month and weekday labels mirror GitHub's familiar calendar.
    first = date.fromordinal(first_sunday)
    for year in range(start.year, end.year + 1):
        for month in range(1, 13):
            month_start = date(year, month, 1)
            label_day = max(start, month_start) if month_start <= end and month_start.month == start.month and year == start.year else month_start
            if start <= label_day <= end:
                col = (label_day.toordinal() - first_sunday) // 7
                draw.text((grid_x + col * stride, 166), month_start.strftime("%b").upper(),
                          font=font(10, True), fill=MUTED)
    for label, weekday_row in [("MON", 1), ("WED", 3), ("FRI", 5)]:
        draw.text((42, grid_y + weekday_row * stride + 2), label, font=font(9, True), fill=MUTED)

    # Genuine calendar values and GitHub's contribution intensity, positioned on the weekday grid.
    positions = {}
    for day, level in contributions.items():
        col = (day.toordinal() - first_sunday) // 7
        row = (day.weekday() + 1) % 7
        x, y = grid_x + col * stride, grid_y + row * stride
        draw.rounded_rectangle((x, y, x + cell - 1, y + cell - 1), radius=2, fill=LEVELS[level])
        if level:
            positions[day] = (x, y, level)

    # Independent breathing highlights on real active days; no added activity, cursor, or path.
    frames = []
    frame_count = 32
    for frame_index in range(frame_count):
        phase = frame_index / frame_count * math.tau
        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        for day, (x, y, level) in positions.items():
            offset = ((day.toordinal() * 47 + level * 23) % 101) / 101 * math.tau
            strength = (math.sin(phase + offset) + 1) / 2
            radius = 2 + int(strength * 4)
            alpha = int(45 + strength * 165)
            glow_draw.rounded_rectangle(
                (x - radius, y - radius, x + cell - 1 + radius, y + cell - 1 + radius),
                radius=4, fill=(*BLUE, alpha)
            )
        glow = glow.filter(ImageFilter.GaussianBlur(2))
        frame = canvas.convert("RGBA")
        frame.alpha_composite(glow)
        # A small, legible accent pulse on stronger genuine activity squares.
        pulse = (math.sin(phase) + 1) / 2
        accent_alpha = int(30 + pulse * 70)
        accent = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        accent_draw = ImageDraw.Draw(accent)
        for x, y, level in positions.values():
            if level >= 2:
                accent_draw.rounded_rectangle((x + 2, y + 2, x + cell - 3, y + cell - 3), radius=2,
                                              fill=(118, 190, 255, accent_alpha))
        frame.alpha_composite(accent)
        frames.append(frame.convert("RGB"))
    return frames

def main():
    total, contributions = fetch_calendar()
    frames = render(total, contributions)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=110, loop=0, optimize=True, disposal=2)
    print(f"Wrote {OUTPUT} with {len(frames)} animated frames from {total:,} public contributions in the last 12 months.")

if __name__ == "__main__":
    main()
