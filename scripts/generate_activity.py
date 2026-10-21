#!/usr/bin/env python3
"""Fetch and render Sameer8549's current-year public GitHub contribution grid."""

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
BG = (7, 11, 20)
INK = (242, 245, 250)
MUTED = (120, 143, 180)
BLUE = (48, 103, 255)
LEVELS = [(21, 31, 49), (22, 57, 117), (27, 84, 172), (39, 119, 226), (103, 190, 255)]


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


def fetch_calendar(year):
    url = f"https://github.com/users/{USERNAME}/contributions?from={year}-01-01&to={year}-12-31"
    request = urllib.request.Request(url, headers={"User-Agent": "Sameer8549-profile-activity/2.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", "replace")
    match = re.search(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    if not match:
        raise RuntimeError("GitHub contribution heading was not found")
    heading = " ".join(re.sub(r"<[^>]+>", " ", match.group(1)).split())
    total_match = re.search(r"([\d,]+)\s+contributions?\s+in\s+(\d{4})", heading)
    if not total_match or int(total_match.group(2)) != year:
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


def render(year, total, contributions, today=None):
    today = today or date.today()
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, WIDTH, 7), fill=BLUE)
    draw.text((42, 28), str(year), font=font(62, True), fill=INK)
    draw.rectangle((42, 105, 212, 111), fill=BLUE)
    draw.text((42, 127), "YEAR TO DATE", font=font(14, True), fill=MUTED)
    draw.text((1158, 42), f"{total:,}", font=font(54, True), fill=INK, anchor="ra")
    draw.text((1158, 105), "PUBLIC CONTRIBUTIONS", font=font(14, True), fill=BLUE, anchor="ra")
    draw.text((600, 27), "ACTIVITY / FIELD RECORD", font=font(13, True), fill=MUTED, anchor="ma")

    cols, rows, cell, gap = 53, 7, 14, 5
    stride = cell + gap
    grid_w = cols * cell + (cols - 1) * gap
    grid_x, grid_y = (WIDTH - grid_w) // 2, 193
    first_sunday = (date(year, 1, 1).weekday() + 1) % 7
    for label, month in [("JAN", 1), ("APR", 4), ("JUL", 7), ("OCT", 10), ("DEC", 12)]:
        first = date(year, month, 1)
        col = (first.timetuple().tm_yday - 1 + first_sunday) // 7
        draw.text((grid_x + col * stride, 168), label, font=font(10, True), fill=MUTED)

    positions = {}
    for day, level in contributions.items():
        if day.year != year or day > today:
            continue
        offset = (day - date(year, 1, 1)).days
        col, row = (offset + first_sunday) // 7, (day.weekday() + 1) % 7
        if col >= cols:
            continue
        x, y = grid_x + col * stride, grid_y + row * stride
        draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=LEVELS[level])
        positions[day] = (x, y, level)

    # Active dates keep their true heatmap colors. Small blue halos breathe at
    # independent phases around those dates, so the graph feels alive without
    # simulating extra commits, a moving cursor, or a progress animation.
    frames, frame_count = [], 32
    for frame_index in range(frame_count):
        phase = (frame_index / frame_count) * math.tau
        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        for day, (x, y, level) in positions.items():
            if not level:
                continue
            seed = (day.toordinal() * 37 + level * 19) % 97
            local = phase + seed / 97 * math.tau
            strength = (math.sin(local) + 1) / 2
            alpha = int((45 + 130 * strength) * (0.72 + level * 0.11))
            radius = 3 + int(4 * strength)
            glow_draw.rounded_rectangle(
                (x - radius, y - radius, x + cell - 1 + radius, y + cell - 1 + radius),
                radius=3,
                fill=(*BLUE, alpha),
            )
        glow = glow.filter(ImageFilter.GaussianBlur(2))
        frame = canvas.convert("RGBA")
        frame.alpha_composite(glow)
        frames.append(frame.convert("RGB"))
    return frames


def main():
    year = date.today().year
    total, contributions = fetch_calendar(year)
    frames = render(year, total, contributions)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=120, loop=0, optimize=True, disposal=2)
    print(f"Wrote {OUTPUT} with {len(frames)} frames from {total:,} public contributions in {year}.")


if __name__ == "__main__":
    main()
