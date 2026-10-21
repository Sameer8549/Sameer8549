#!/usr/bin/env python3
"""Animate the exact GitHub activity grid shown in the user's supplied profile screenshot.

The GitHub profile view reports 90 contributions. Its unauthenticated public calendar
feed differs, so this image is an explicitly dated profile snapshot instead of a misleading
live feed. Refresh by replacing the matrix from a newer profile screenshot.
"""

from datetime import date
from math import sin, tau
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "activity.gif"
WIDTH, HEIGHT = 1200, 360
BG = (7, 11, 20)
INK = (242, 245, 250)
MUTED = (153, 173, 208)
BLUE = (40, 87, 255)
LEVELS = [(21, 27, 35), (18, 62, 42), (12, 99, 57), (16, 139, 74), (45, 194, 105)]
# 53 calendar columns x 7 weekdays, sampled from the supplied 90-contribution GitHub profile view.
ROWS = [
    "00000000000000000000000000000001000000200000000000200",
    "00200000000000000020000000000000001000000010000200000",
    "00000000000000000000000000000000000010200010000400000",
    "00000000000000000000000100000000400000200000004000121",
    "00000000010000000000000200000000101000000000000000000",
    "00000000000000000000100000000000011000000110000000400",
    "00000000000000000000000000000000000002100102000000100",
]
TOTAL = 90
START = date(2025, 10, 19)  # First Sunday visible in the supplied October-to-October calendar.
END = date(2026, 10, 21)


def font(size, bold=False, mono=False):
    options = [
        Path("C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf") if mono else
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf" if mono else
             ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")),
    ]
    for candidate in options:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def render():
    if len(ROWS) != 7 or any(len(row) != 53 for row in ROWS):
        raise ValueError("Contribution snapshot must contain 53 columns and 7 weekdays")
    cells = [(col, row, int(ROWS[row][col])) for col in range(53) for row in range(7)]
    width, gap = 14, 5
    stride = width + gap
    grid_w = 53 * width + 52 * gap
    grid_x, grid_y = (WIDTH - grid_w) // 2, 202
    frames = []
    for frame_index in range(40):
        canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
        d = ImageDraw.Draw(canvas)
        d.rectangle((0, 0, WIDTH, 7), fill=BLUE)
        d.text((42, 22), "90", font=font(55, True), fill=INK)
        d.text((44, 83), "CONTRIBUTIONS / LAST 12 MONTHS", font=font(14, True, mono=True), fill=BLUE)
        d.text((1158, 28), "PROFILE SNAPSHOT", font=font(13, True, mono=True), fill=MUTED, anchor="ra")
        d.text((1158, 56), "21 OCT 2026 · GITHUB", font=font(15, True), fill=INK, anchor="ra")
        d.line((42, 121, 1158, 121), fill=(51, 65, 99), width=1)
        d.text((42, 143), "PROFILE CONTRIBUTION RECORD", font=font(11, True, mono=True), fill=MUTED)
        months = [(2025, 10), *[(2026, month) for month in range(1, 11)]]
        for year, month in months:
            month_date = date(year, month, 1)
            label_date = max(START, month_date) if (year, month) == (START.year, START.month) else month_date
            col = (label_date - START).days // 7 + (0 if label_date == START else 1)
            d.text((grid_x + col * stride, 174), label_date.strftime("%b").upper(),
                   font=font(10, True), fill=MUTED)
        for label, row in [("MON", 1), ("WED", 3), ("FRI", 5)]:
            d.text((42, grid_y + row * stride + 2), label, font=font(9, True), fill=MUTED)
        d.text((884, 338), "LESS", font=font(9, True), fill=MUTED)
        for index, color in enumerate(LEVELS):
            x = 927 + index * 22
            d.rounded_rectangle((x, 337, x + 14, 351), radius=2, fill=color)
        d.text((1050, 338), "MORE", font=font(9, True), fill=MUTED)
        active = []
        for col, row, level in cells:
            x, y = grid_x + col * stride, grid_y + row * stride
            d.rounded_rectangle((x, y, x + width - 1, y + width - 1), radius=2,
                                fill=LEVELS[level])
            if level:
                active.append((col, row, level, x, y))
        # Brighter blue light breathes across the exact active cells; no fabricated days or counts.
        glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        phase = frame_index / 40 * tau
        for col, row, level, x, y in active:
            seed = (col * 31 + row * 47 + level * 13) % 97
            strength = (sin(phase + seed / 97 * tau) + 1) / 2
            radius = 1 + round(strength * 4)
            alpha = int(25 + 135 * strength)
            gd.rounded_rectangle((x - radius, y - radius, x + width - 1 + radius, y + width - 1 + radius),
                                 radius=4, fill=(*BLUE, alpha))
        canvas = canvas.convert("RGBA")
        canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(2)))
        frames.append(canvas.convert("RGB"))
    return frames


def main():
    frames = render()
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=95,
                   loop=0, optimize=True, disposal=2)
    print(f"Wrote {OUTPUT}: animated 90-contribution profile snapshot, 40 frames.")

if __name__ == "__main__":
    main()
