#!/usr/bin/env python3
"""Animate the 2026 GitHub contribution calendar captured on 21 October 2026.

Cell levels and the yearly total are from GitHub's public contribution calendar. The cells
remain fixed; the moving quarter frame is a visual focus, not live or fabricated activity.
"""

from datetime import date
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
# 53 weeks x 7 weekdays, mapped from GitHub's 2026 contribution calendar (level 0–4).
ROWS = [
    "00000000000000000000010000001000000000002000000000000",
    "00000000200000000000000010100000100002000000000000000",
    "00000000000000000000000000002000100004001000000000000",
    "00000000000000000000004010002000000040000210000000000",
    "00000000000002000000001000000000000000000000000000000",
    "00000000001000000000000010000001100000004000000000000",
    "00000000000000000000000000021001010000001000000000000",
]
TOTAL = 84
GRID_START = date(2025, 12, 28)  # Sunday before the first day of 2026.
SNAPSHOT_DATE = date(2026, 10, 21)


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
        d.text((42, 22), str(TOTAL), font=font(55, True), fill=BLUE)
        d.text((44, 83), "CONTRIBUTIONS IN 2026", font=font(14, True, mono=True), fill=INK)
        d.text((1158, 28), "PROFILE SNAPSHOT", font=font(13, True, mono=True), fill=MUTED, anchor="ra")
        d.text((1158, 56), f"{SNAPSHOT_DATE:%d %b %Y} · GITHUB", font=font(15, True), fill=INK, anchor="ra")
        d.line((42, 121, 1158, 121), fill=(160, 183, 255), width=1)
        focus = (frame_index // (frame_count // 4)) % 4
        windows = [("JAN — MAR 26", 0, 13), ("APR — JUN 26", 13, 26),
                   ("JUL — SEP 26", 26, 39), ("OCT — DEC 26", 39, 53)]
        window_label, first_col, last_col = windows[focus]
        d.text((42, 143), "PROFILE CONTRIBUTION RECORD", font=font(11, True, mono=True), fill=INK)
        d.text((1158, 143), f"WINDOW / {window_label}", font=font(11, True, mono=True),
               fill=INK, anchor="ra")
        month_marks = [(date(2026, month, 1).strftime("%b").upper(),
                        (date(2026, month, 1) - GRID_START).days // 7)
                       for month in range(1, 13)]
        for label, col in month_marks:
            d.text((grid_x + col * stride, 174), label, font=font(10, True), fill=INK)
        for label, row in [("MON", 1), ("WED", 3), ("FRI", 5)]:
            d.text((42, grid_y + row * stride + 2), label, font=font(9, True), fill=INK)
        left = grid_x + first_col * stride - 4
        right = grid_x + (last_col - 1) * stride + width + 4
        d.rectangle((left, 165, right, grid_y + 7 * stride - 2), outline=INK, width=2)
        d.text((884, 338), "LESS", font=font(9, True), fill=INK)
        for index, color in enumerate(LEVELS):
            x = 927 + index * 22
            d.rounded_rectangle((x, 337, x + 14, 351), radius=2, fill=color)
        d.text((1050, 338), "MORE", font=font(9, True), fill=INK)
        for col, row, level in cells:
            x, y = grid_x + col * stride, grid_y + row * stride
            d.rounded_rectangle((x, y, x + width - 1, y + width - 1), radius=2,
                                fill=LEVELS[level])
        # The selected quarter frames existing cells; their values never change.
        # This is a visual focus over the dated GitHub snapshot, not live activity.
        for col, row, level in cells:
            if level and first_col <= col < last_col:
                x, y = grid_x + col * stride, grid_y + row * stride
                d.rounded_rectangle((x - 1, y - 1, x + width, y + width),
                                    radius=3, outline=INK, width=2)
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
