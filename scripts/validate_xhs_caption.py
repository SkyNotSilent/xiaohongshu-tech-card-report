#!/usr/bin/env python3
"""Validate Xiaohongshu title, caption, and hashtag limits."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def strip_md_prefix(line: str) -> str:
    line = line.strip()
    line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line)
    return line.strip()


def section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.I | re.M)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", text[start:], flags=re.M)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def extract_titles(text: str) -> list[str]:
    candidates = []
    title_block = section(text, "Title options") or section(text, "标题") or section(text, "标题选项")
    for line in title_block.splitlines():
        clean = strip_md_prefix(line)
        if clean:
            candidates.append(clean)
    if candidates:
        return candidates
    for line in text.splitlines():
        if line.lower().startswith("title:") or line.startswith("标题：") or line.startswith("标题:"):
            value = re.sub(r"^(title:|标题[:：])", "", line, flags=re.I).strip()
            if value:
                candidates.append(value)
    return candidates


def extract_caption(text: str) -> str:
    body = section(text, "Caption") or section(text, "正文") or section(text, "文案")
    if body:
        return body.strip()
    lines = []
    in_body = False
    for line in text.splitlines():
        if re.match(r"^(caption|正文|文案)[:：]\s*", line, flags=re.I):
            in_body = True
            lines.append(re.sub(r"^(caption|正文|文案)[:：]\s*", "", line, flags=re.I))
            continue
        if in_body and line.startswith("## "):
            break
        if in_body:
            lines.append(line)
    return "\n".join(lines).strip()


def extract_tags(text: str) -> list[str]:
    tag_block = section(text, "Hashtags") or section(text, "Tags") or section(text, "标签")
    search_area = tag_block if tag_block else text
    tags = re.findall(r"#[\w\u4e00-\u9fff-]+", search_area)
    deduped = []
    seen = set()
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            deduped.append(tag)
    return deduped


def count_chars(value: str) -> int:
    return len(re.sub(r"\s+", "", value))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Xiaohongshu caption limits.")
    parser.add_argument("caption_file")
    parser.add_argument("--max-title", type=int, default=20)
    parser.add_argument("--max-body", type=int, default=1000)
    parser.add_argument("--min-tags", type=int, default=6)
    parser.add_argument("--max-tags", type=int, default=10)
    args = parser.parse_args()

    text = Path(args.caption_file).read_text(encoding="utf-8")
    titles = extract_titles(text)
    caption = extract_caption(text)
    tags = extract_tags(text)
    errors = []
    warnings = []

    if not titles:
        errors.append("No title options found.")
    for title in titles:
        length = count_chars(title)
        if length > args.max_title:
            errors.append(f"Title too long ({length}>{args.max_title}): {title}")

    body_length = count_chars(caption)
    if not caption:
        errors.append("No caption body found.")
    elif body_length > args.max_body:
        errors.append(f"Caption body too long ({body_length}>{args.max_body}).")

    if len(tags) < args.min_tags:
        errors.append(f"Too few hashtags ({len(tags)}<{args.min_tags}).")
    if len(tags) > args.max_tags:
        errors.append(f"Too many hashtags ({len(tags)}>{args.max_tags}).")

    if len(set(tags)) != len(tags):
        warnings.append("Duplicate hashtags detected.")

    print(f"titles={len(titles)} caption_chars={body_length} tags={len(tags)}")
    for title in titles:
        print(f"title[{count_chars(title)}]: {title}")
    if tags:
        print("tags: " + " ".join(tags))
    for warning in warnings:
        print("warning: " + warning, file=sys.stderr)
    if errors:
        for error in errors:
            print("error: " + error, file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
