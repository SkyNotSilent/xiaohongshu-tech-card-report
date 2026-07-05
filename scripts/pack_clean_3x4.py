#!/usr/bin/env python3
"""Validate 3:4 carousel PNGs and create a clean zip."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover
    print("Pillow is required. Install pillow in the active Python environment.", file=sys.stderr)
    raise SystemExit(2) from exc


CARD_RE = re.compile(r"^\d{2}[-_].*\.png$", re.I)


def is_ratio(size: tuple[int, int], target: float, tolerance: float) -> bool:
    width, height = size
    return height > 0 and abs((width / height) - target) <= tolerance


def scan_images(folder: Path, target: float, tolerance: float) -> tuple[list[dict], list[dict]]:
    valid = []
    invalid = []
    for path in sorted(folder.iterdir()):
        if path.is_dir() or path.suffix.lower() != ".png":
            continue
        if not CARD_RE.match(path.name):
            invalid.append({"file": path.name, "reason": "filename does not match NN-name.png"})
            continue
        try:
            with Image.open(path) as image:
                size = image.size
        except Exception as exc:
            invalid.append({"file": path.name, "reason": f"cannot open image: {exc}"})
            continue
        entry = {
            "file": path.name,
            "path": str(path),
            "width": size[0],
            "height": size[1],
            "ratio": round(size[0] / size[1], 6) if size[1] else None,
        }
        if is_ratio(size, target, tolerance):
            valid.append(entry)
        else:
            entry["reason"] = f"not 3:4 within tolerance {tolerance}"
            invalid.append(entry)
    return valid, invalid


def create_contact_sheet(valid: list[dict], out: Path, thumb_w: int = 217, thumb_h: int = 290) -> None:
    if not valid:
        return
    cols = 4
    pad = 24
    label_h = 32
    rows = (len(valid) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad), (245, 247, 250))
    draw = ImageDraw.Draw(sheet)
    for index, entry in enumerate(valid):
        image = Image.open(entry["path"]).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + (index % cols) * (thumb_w + pad)
        y = pad + (index // cols) * (thumb_h + label_h + pad)
        sheet.paste(image, (x + (thumb_w - image.width) // 2, y))
        draw.text((x, y + thumb_h + 6), entry["file"], fill=(20, 30, 45))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=92)


def create_zip(valid: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for entry in valid:
            archive.write(entry["path"], entry["file"])


def write_manifest(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Package only valid 3:4 Xiaohongshu PNG cards.")
    parser.add_argument("--input", required=True, help="Directory containing card PNG files.")
    parser.add_argument("--out", required=True, help="Output clean zip path.")
    parser.add_argument("--manifest", help="Optional manifest JSON path.")
    parser.add_argument("--contact-sheet", help="Optional contact sheet JPG path.")
    parser.add_argument("--expected", type=int, default=11)
    parser.add_argument("--ratio", default="3:4")
    parser.add_argument("--tolerance", type=float, default=0.001)
    parser.add_argument("--fail-on-invalid", action="store_true")
    args = parser.parse_args()

    left, right = args.ratio.split(":", 1)
    target = float(left) / float(right)
    folder = Path(args.input)
    valid, invalid = scan_images(folder, target, args.tolerance)
    valid.sort(key=lambda entry: entry["file"])

    payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(folder),
        "zip": str(Path(args.out)),
        "target_ratio": args.ratio,
        "tolerance": args.tolerance,
        "expected": args.expected,
        "valid_count": len(valid),
        "invalid_count": len(invalid),
        "valid": valid,
        "invalid": invalid,
    }

    if args.manifest:
        write_manifest(Path(args.manifest), payload)
    if args.contact_sheet:
        create_contact_sheet(valid, Path(args.contact_sheet))

    errors = []
    if len(valid) != args.expected:
        errors.append(f"expected {args.expected} valid PNGs, found {len(valid)}")
    if args.fail_on_invalid and invalid:
        errors.append(f"found {len(invalid)} invalid PNG(s)")
    if errors:
        for item in invalid:
            print(f"invalid: {item}", file=sys.stderr)
        for error in errors:
            print("error: " + error, file=sys.stderr)
        return 1

    create_zip(valid, Path(args.out))
    print(f"zip={args.out}")
    print(f"valid={len(valid)} invalid={len(invalid)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
