#!/usr/bin/env python3
"""Convert eDiary exported files into Obsidian markdown notes."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path


DATE_PATTERNS = [
    re.compile(r"^(?P<y>20\d{2})[-_.年](?P<m>\d{1,2})[-_.月](?P<d>\d{1,2})"),
    re.compile(r"^(?P<y>20\d{2})(?P<m>\d{2})(?P<d>\d{2})$"),
]


def parse_date_from_name(path: Path) -> datetime | None:
    stem = path.stem
    for pattern in DATE_PATTERNS:
        match = pattern.match(stem)
        if not match:
            continue
        year = int(match.group("y"))
        month = int(match.group("m"))
        day = int(match.group("d"))
        return datetime(year, month, day)
    return None


def rtf_to_text(content: str) -> str:
    text = content
    text = re.sub(r"\\par[d]?", "\n", text)
    text = re.sub(r"\\line", "\n", text)
    text = re.sub(r"\\tab", "\t", text)
    text = re.sub(r"\\'[0-9a-fA-F]{2}", lambda m: bytes.fromhex(m.group(0)[2:]).decode("latin-1", errors="ignore"), text)
    text = re.sub(r"\\[a-zA-Z]+\d* ?", "", text)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def read_export_file(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"{\\rtf"):
        return rtf_to_text(raw.decode("latin-1", errors="ignore"))
    for encoding in ("utf-8-sig", "utf-16", "gbk"):
        try:
            return raw.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="ignore").strip()


def target_markdown_path(output_dir: Path, source: Path, body: str) -> Path:
    date = parse_date_from_name(source)
    if date:
        return output_dir / f"{date:%Y-%m-%d}.md"

    first_line = next((line.strip() for line in body.splitlines() if line.strip()), source.stem)
    safe = re.sub(r'[\\/:*?"<>|]', "-", first_line)[:60] or source.stem
    return output_dir / f"{safe}.md"


def convert_file(source: Path, output_dir: Path, move_source: bool) -> Path:
    body = read_export_file(source)
    if not body:
        raise ValueError(f"empty export file: {source}")

    target = target_markdown_path(output_dir, source, body)
    if target.exists():
        stem = target.stem
        suffix = 2
        while target.exists():
            target = output_dir / f"{stem}-{suffix}.md"
            suffix += 1

    date = parse_date_from_name(source)
    header = f"# {date:%Y-%m-%d}\n\n" if date else ""
    target.write_text(header + body + "\n", encoding="utf-8")

    if move_source:
        done_dir = source.parent / "_done"
        done_dir.mkdir(exist_ok=True)
        shutil.move(str(source), str(done_dir / source.name))

    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(r"E:\Project\Note\Me\日记\_export"),
        help="Folder containing eDiary exported txt/rtf/html files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(r"E:\Project\Note\Me\日记"),
        help="Obsidian markdown output folder",
    )
    parser.add_argument("--move", action="store_true", help="Move processed exports to _done/")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    patterns = ("*.txt", "*.rtf", "*.html", "*.htm")
    files = sorted({p for pattern in patterns for p in args.input.glob(pattern)})

    if not files:
        print(f"No export files found in {args.input}")
        print("Export from eDiary first, then rerun this script.")
        return

    converted = 0
    for source in files:
        target = convert_file(source, args.output, args.move)
        print(f"{source.name} -> {target}")
        converted += 1

    print(f"Done. Converted {converted} file(s) into {args.output}")


if __name__ == "__main__":
    main()
