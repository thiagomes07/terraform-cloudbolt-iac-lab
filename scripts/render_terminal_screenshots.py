#!/usr/bin/env python3
"""Render captured command output as terminal-style PNG evidence."""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Supplemental/Monaco.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load_font(size: int) -> ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def clean(text: str) -> str:
    text = ANSI_RE.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip("\n")


def wrap_lines(text: str, max_cols: int) -> list[str]:
    lines: list[str] = []
    for line in clean(text).splitlines() or [""]:
        if len(line) <= max_cols:
            lines.append(line)
            continue
        lines.extend(
            textwrap.wrap(
                line,
                width=max_cols,
                replace_whitespace=False,
                drop_whitespace=False,
                break_long_words=True,
            )
        )
    return lines


def render(input_path: Path, output_path: Path, max_cols: int) -> None:
    font = load_font(18)
    title_font = load_font(15)
    lines = wrap_lines(input_path.read_text(encoding="utf-8"), max_cols)

    sample = "M" * max_cols
    bbox = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), sample, font=font)
    char_width = max(10, (bbox[2] - bbox[0]) // max_cols)
    line_height = 27
    padding_x = 28
    padding_y = 30
    chrome_height = 42

    width = min(1800, max(980, (char_width * max_cols) + (padding_x * 2)))
    height = chrome_height + (padding_y * 2) + (line_height * len(lines))

    image = Image.new("RGB", (width, height), "#101418")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, chrome_height), fill="#20262d")
    for index, color in enumerate(["#ff5f57", "#ffbd2e", "#28c840"]):
        draw.ellipse((24 + index * 28, 14, 38 + index * 28, 28), fill=color)
    draw.text((116, 12), input_path.name, font=title_font, fill="#c8d1da")

    y = chrome_height + padding_y
    for line in lines:
        fill = "#8bd5ff" if line.startswith("$ ") else "#f2f5f7"
        draw.text((padding_x, y), line, font=font, fill=fill)
        y += line_height

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("--max-cols", type=int, default=112)
    args = parser.parse_args()

    for input_path in sorted(args.evidence_dir.glob("*.txt")):
        output_path = args.image_dir / f"{input_path.stem}.png"
        render(input_path, output_path, args.max_cols)
        print(f"rendered {output_path}")


if __name__ == "__main__":
    main()

