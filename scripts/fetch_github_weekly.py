#!/usr/bin/env python3
"""Fetch GitHub Trending weekly repositories for Xiaohongshu card packages."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


TRENDING_URL = "https://github.com/trending?since=weekly"
UA = "Mozilla/5.0 (Codex xiaohongshu-tech-card-report)"


def get_text(url: str, *, accept: str | None = None, timeout: int = 25, retries: int = 3) -> str:
    headers = {"User-Agent": UA}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read()
            return raw.decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(2 ** (attempt - 1), 4))
    raise last_error if last_error else RuntimeError(f"Failed to fetch {url}")


def get_json(url: str, timeout: int = 25) -> dict:
    return json.loads(get_text(url, accept="application/vnd.github+json", timeout=timeout))


def clean_lines(markup: str) -> list[str]:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", markup, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "\n", text)
    lines = []
    for line in html.unescape(text).splitlines():
        clean = re.sub(r"\s+", " ", line).strip()
        if clean:
            lines.append(clean)
    return lines


def parse_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value.replace(",", "").strip())
    except ValueError:
        return None


def compact(value: str | None, limit: int = 220) -> str:
    if not value:
        return ""
    value = re.sub(r"\s+", " ", value).strip()
    return textwrap.shorten(value, width=limit, placeholder="...")


def extract_repo_from_block(block: str) -> tuple[str, str] | None:
    h2 = re.search(r"<h2\b.*?</h2>", block, flags=re.I | re.S)
    search_area = h2.group(0) if h2 else block
    for href in re.findall(r'href="([^"]+)"', search_area):
        match = re.match(r"^/([^/\s]+)/([^/\s#?]+)$", html.unescape(href))
        if match:
            return match.group(1), match.group(2)
    for href in re.findall(r'href="([^"]+)"', block):
        match = re.match(r"^/([^/\s]+)/([^/\s#?]+)$", html.unescape(href))
        if match:
            return match.group(1), match.group(2)
    return None


def parse_trending(html_text: str, limit: int) -> list[dict]:
    blocks = re.findall(r"<article\b[^>]*Box-row[^>]*>(.*?)</article>", html_text, flags=re.I | re.S)
    repos: list[dict] = []
    seen: set[str] = set()
    for block in blocks:
        repo = extract_repo_from_block(block)
        if not repo:
            continue
        owner, name = repo
        full_name = f"{owner}/{name}"
        if full_name in seen:
            continue
        seen.add(full_name)
        lines = clean_lines(block)
        text = " ".join(lines)
        weekly = parse_int((re.search(r"([\d,]+)\s+stars?\s+this\s+week", text, flags=re.I) or [None, None])[1])
        star_matches = [parse_int(m) for m in re.findall(r"([\d,]+)\s+stars\b(?!\s+this\s+week)", text, flags=re.I)]
        fork_matches = [parse_int(m) for m in re.findall(r"([\d,]+)\s+forks?", text, flags=re.I)]
        description = ""
        for line in lines:
            if line in {owner, name, full_name}:
                continue
            if "stars this week" in line.lower() or line.lower().endswith("stars") or line.lower().endswith("forks"):
                continue
            if line.lower() in {"built by", "sponsor"}:
                continue
            if len(line) > 20:
                description = line
                break
        repos.append(
            {
                "rank": len(repos) + 1,
                "owner": owner,
                "name": name,
                "full_name": full_name,
                "url": f"https://github.com/{full_name}",
                "language": "",
                "description": compact(description),
                "stars": star_matches[0] if star_matches else None,
                "forks": fork_matches[0] if fork_matches else None,
                "stars_this_week": weekly,
                "stars_this_week_display": f"+{weekly:,}" if weekly is not None else "",
            }
        )
        if len(repos) >= limit:
            break
    return repos


def summarize_readme(owner: str, repo: str, default_branch: str | None) -> str:
    branch = default_branch or "main"
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{urllib.parse.quote(branch)}/README.md"
    try:
        text = get_text(url, timeout=15)
    except Exception:
        return ""
    lines = []
    in_code = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line:
            continue
        if line.startswith(("#", "!", "[!", "<", "|", "-", "*", ">")):
            continue
        if re.search(r"https?://|<img|badge|shields\.io", line, flags=re.I):
            continue
        lines.append(line)
        if sum(len(x) for x in lines) >= 260:
            break
    return compact(" ".join(lines), 260)


def enrich_repo(repo: dict, *, no_api: bool = False) -> dict:
    if no_api:
        return repo
    owner, name = repo["owner"], repo["name"]
    api_url = f"https://api.github.com/repos/{owner}/{name}"
    try:
        data = get_json(api_url)
    except Exception as exc:
        repo["api_error"] = str(exc)
        return repo
    repo["language"] = data.get("language") or repo.get("language") or ""
    repo["description"] = compact(data.get("description") or repo.get("description"))
    repo["stars"] = data.get("stargazers_count") or repo.get("stars")
    repo["forks"] = data.get("forks_count") or repo.get("forks")
    repo["topics"] = data.get("topics") or []
    repo["default_branch"] = data.get("default_branch")
    repo["homepage"] = data.get("homepage") or ""
    repo["readme_summary"] = summarize_readme(owner, name, repo.get("default_branch"))
    return repo


def write_sources_md(path: Path, payload: dict) -> None:
    lines = [
        "# Sources",
        "",
        f"- Access date: {payload['access_date']}",
        f"- Trending URL: {payload['trending_url']}",
        "",
        "| Rank | Repository | Language | Stars | Forks | Stars this week | URL | Verified fact used |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for repo in payload["repositories"]:
        fact = compact(repo.get("description") or repo.get("readme_summary") or "", 90)
        lines.append(
            "| {rank} | {name} | {lang} | {stars} | {forks} | {weekly} | {url} | {fact} |".format(
                rank=repo["rank"],
                name=repo["full_name"],
                lang=repo.get("language") or "",
                stars=repo.get("stars") if repo.get("stars") is not None else "",
                forks=repo.get("forks") if repo.get("forks") is not None else "",
                weekly=repo.get("stars_this_week_display") or "",
                url=repo["url"],
                fact=fact.replace("|", "/"),
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch GitHub Trending weekly Top repositories.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--out", required=True, help="Output JSON path.")
    parser.add_argument("--sources-md", help="Optional sources.md path.")
    parser.add_argument("--fixture-html", help="Read Trending HTML from a local file instead of live GitHub.")
    parser.add_argument("--no-api", action="store_true", help="Do not call the GitHub repo API/readme endpoints.")
    parser.add_argument("--allow-missing-weekly", action="store_true")
    args = parser.parse_args()

    if args.fixture_html:
        html_text = Path(args.fixture_html).read_text(encoding="utf-8")
        source = f"fixture:{args.fixture_html}"
    else:
        html_text = get_text(TRENDING_URL)
        source = TRENDING_URL

    repos = parse_trending(html_text, args.limit)
    if len(repos) < args.limit:
        print(f"Expected {args.limit} repositories, found {len(repos)}.", file=sys.stderr)
        return 2
    for repo in repos:
        enrich_repo(repo, no_api=args.no_api)

    missing_weekly = [repo["full_name"] for repo in repos if repo.get("stars_this_week") is None]
    if missing_weekly and not args.allow_missing_weekly:
        print("Missing stars this week for: " + ", ".join(missing_weekly), file=sys.stderr)
        return 3

    payload = {
        "source": source,
        "trending_url": TRENDING_URL,
        "access_date": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "repositories": repos,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.sources_md:
        write_sources_md(Path(args.sources_md), payload)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
