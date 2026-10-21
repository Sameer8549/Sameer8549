#!/usr/bin/env python3
"""Animate the exact GitHub activity grid shown in the user's supplied profile screenshot.

The GitHub profile view reports 90 contributions. Its unauthenticated public calendar
feed differs, so this image is an explicitly dated profile snapshot instead of a misleading
live feed. Refresh by replacing the matrix from a newer profile screenshot.
"""

from datetime import date
from math import cos, pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "activity.gif"
WIDTH, HEIGHT = 1200, 360
BG = (43, 82, 250)
INK = (244, 246, 255)
MUTED = (181, 198, 255)
BLUE = (8, 19, 68)
LEVELS = [(8, 19, 68), (13, 34, 116), (22, 51, 160), (34, 68, 201), (132, 160, 255)]
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


def render_frames():
    if len(ROWS) != 7 or any(len(row) != 53 for row in ROWS):
        raise ValueError("Contribution snapshot must contain 53 columns and 7 weekdays")
    cells = [(col, row, int(ROWS[row][col])) for col in range(53) for row in range(7)]
    width, gap = 14, 5
    stride = width + gap
    grid_w = 53 * width + 52 * gap
    grid_x, grid_y = (WIDTH - grid_w) // 2, 202
    frames = []
    frame_count = 40
    for frame_index in range(frame_count):
        canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
        d = ImageDraw.Draw(canvas)
        d.text((42, 22), "90", font=font(55, True), fill=BLUE)
        d.text((44, 83), "CONTRIBUTIONS / LAST 12 MONTHS", font=font(14, True, mono=True), fill=INK)
        d.text((1158, 28), "PROFILE SNAPSHOT", font=font(13, True, mono=True), fill=MUTED, anchor="ra")
        d.text((1158, 56), "21 OCT 2026 · GITHUB", font=font(15, True), fill=INK, anchor="ra")
        d.line((42, 121, 1158, 121), fill=(160, 183, 255), width=1)
        d.text((42, 143), "PROFILE CONTRIBUTION RECORD", font=font(11, True, mono=True), fill=INK)
        month_marks = [("OCT", 0), ("NOV", 4), ("DEC", 9), ("JAN", 13), ("FEB", 17),
                       ("MAR", 21), ("APR", 26), ("MAY", 30), ("JUN", 34), ("JUL", 39),
                       ("AUG", 43), ("SEP", 47), ("OCT", 51)]
        for label, col in month_marks:
            d.text((grid_x + col * stride, 174), label, font=font(10, True), fill=INK)
        for label, row in [("MON", 1), ("WED", 3), ("FRI", 5)]:
            d.text((42, grid_y + row * stride + 2), label, font=font(9, True), fill=INK)
        d.text((884, 338), "LESS", font=font(9, True), fill=INK)
        for index, color in enumerate(LEVELS):
            x = 927 + index * 22
            d.rounded_rectangle((x, 337, x + 14, 351), radius=2, fill=color)
        d.text((1050, 338), "MORE", font=font(9, True), fill=INK)
        active = []
        for col, row, level in cells:
            x, y = grid_x + col * stride, grid_y + row * stride
            d.rounded_rectangle((x, y, x + width - 1, y + width - 1), radius=2,
                                fill=LEVELS[level])
            if level:
                active.append((col, row, level, x, y))
        # Four fixed cells breathe in place. The dated contribution data never moves
        # or changes intensity, and the animation does not trace a snake path.
        if active:
            picks = [active[k] for k in (5, 17, 31, 44) if k < len(active)]
            for pulse_index, (_, _, _, fx, fy) in enumerate(picks):
                phase = pulse_index * frame_count // max(1, len(picks))
                wave = (1 + cos(2 * pi * (frame_index - phase) / frame_count)) / 2
                channel = int(88 + 130 * wave)
                glow = (channel, min(235, channel + 22), 255)
                d.rounded_rectangle((fx - 2, fy - 2, fx + width + 1, fy + width + 1),
                                    radius=3, outline=glow, width=2)
        frames.append(canvas)
    return frames


def render():
    return render_frames()


def main():
    frames = render_frames()
    frames[0].save(OUTPUT, save_all=True, append_images=frames[1:], duration=240,
                   loop=0, optimize=True, disposal=2)
    print(f"Wrote {OUTPUT}: animated 90-contribution profile snapshot, 40 frames.")

if __name__ == "__main__":
    main()
