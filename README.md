# Xiaohongshu Tech Card Report

GitHub 本周热榜小红书图文生成 Skill。把 GitHub Trending Weekly Top10 自动整理成可发布的小红书卡片、标题、正文、标签和 3:4 图片包。

Generate publish-ready Xiaohongshu carousel packages for GitHub weekly hot repositories, AI reports, and developer-tool roundups.

**Search keywords**: GitHub 热榜小红书, GitHub 本周热榜, GitHub Trending 周榜, GitHub 开源项目榜单, 小红书图文卡片, AI 工具周报, 开源项目周报, Codex skill, Xiaohongshu carousel, GitHub weekly hot list.

This Codex skill turns a request like:

```text
帮我做一个 GitHub 本周热榜的小红书图文笔记
```

or:

```text
做一套紫色主题的 GitHub 本周热榜小红书卡片
```

into a full production package:

- current GitHub Trending weekly Top10 data;
- verified repository source records;
- card-by-card Chinese copy;
- JSON image prompts for a locked frosted-glass visual system;
- 1 cover image + 10 ranked detail images;
- strict 3:4 validation;
- a clean zip containing only valid PNG cards;
- Xiaohongshu title options, caption, and hashtags.

If you create AI/devtool content for Xiaohongshu, bookmark this repo for repeatable weekly GitHub hot-list production.

## Preview

![GitHub weekly hot Xiaohongshu carousel contact sheet](examples/github-weekly-hot-contact-sheet.jpg)

## What It Solves

Most GitHub trend posts fail in one of three ways:

- the ranking data is stale or manually invented;
- the card design drifts between pages;
- the final package contains wrong-size drafts, contact sheets, or old images.

This skill makes the workflow repeatable. It fetches live weekly data, locks the Xiaohongshu card format, validates image ratios, and only packages final 3:4 PNGs.

## Features

- **Live GitHub weekly data**: starts from `https://github.com/trending?since=weekly`.
- **Source-backed cards**: records repo URL, language, total stars, forks, stars this week, and README/API summary.
- **Xiaohongshu-ready copy**: keeps titles short, captions compact, and hashtags relevant.
- **Stable visual system**: white frosted-glass cards, rank badges, colored metrics, and strict page semantics.
- **Purple theme branch**: deterministic purple frosted-glass rendering for text-heavy GitHub weekly cards where numbers must stay exact.
- **Clean image packaging**: final zip includes only validated 3:4 PNG files.
- **Reusable scripts**: fetch data, validate captions, and package final cards.

## Who Should Bookmark This

- Xiaohongshu tech creators who post GitHub / AI / developer-tool roundups.
- AI content operators who need a repeatable weekly visual workflow.
- Developers building verified card reports from GitHub Trending data.
- Teams that need source-backed Chinese cards instead of manually rewritten screenshots.

## Copy-Paste Prompts

Generate a standard GitHub weekly hot Xiaohongshu package:

```text
帮我做一个 GitHub 本周热榜的小红书图文笔记
```

Generate the purple theme version:

```text
做一套紫色主题的 GitHub 本周热榜小红书卡片
```

Copy-only mode:

```text
先别生图，先给我 GitHub 本周热榜的小红书卡片文案和标题标签
```

## SEO Keywords

GitHub Trending, GitHub weekly hot list, GitHub weekly Top10, Xiaohongshu carousel, Xiaohongshu cards, 小红书图文笔记, 小红书卡片模板, GitHub 热榜, GitHub 本周热榜, GitHub 开源项目周榜, AI tools, developer tools, open source weekly report, Codex skill, AI content workflow, AI 内容生产, 技术内容运营.

## Repository Structure

```text
SKILL.md
references/
  github-weekly-hot-xhs.md
  github-weekly-purple-theme-xhs.md
  xhs-publishing-limits.md
scripts/
  create_xhs_card_job.js
  fetch_github_weekly.py
  validate_xhs_caption.py
  pack_clean_3x4.py
templates/
  cards.md
evals/
  evals.json
  fixtures/trending-weekly-sample.html
examples/
  github-weekly-hot-contact-sheet.jpg
  github-weekly-hot-case.md
```

## Quick Start

Install this folder as a Codex skill under:

```text
~/.codex/skills/xiaohongshu-tech-card-report
```

Then ask Codex:

```text
帮我做一个 GitHub 本周热榜的小红书图文笔记
```

Default behavior:

1. Fetch the latest GitHub Trending weekly Top10.
2. Create source and selection records.
3. Generate `cards.md`, `xhs_caption.md`, and `visual_prompts.json`.
4. Generate 11 images with the built-in image generation tool.
5. Validate every image is 3:4.
6. Build `clean-3x4-only.zip`.

## Scripts

Fetch GitHub weekly data:

```bash
python scripts/fetch_github_weekly.py \
  --limit 10 \
  --out 00_source/github-weekly.json \
  --sources-md 00_source/sources.md
```

Validate Xiaohongshu caption limits:

```bash
python scripts/validate_xhs_caption.py 02_cards/xhs_caption.md
```

Create a clean 3:4-only image zip:

```bash
python scripts/pack_clean_3x4.py \
  --input 03_images \
  --out clean-3x4-only.zip \
  --manifest manifest.json \
  --contact-sheet contact-sheet.jpg \
  --expected 11 \
  --fail-on-invalid
```

`pack_clean_3x4.py` requires Pillow. In Codex Desktop, use the bundled Python from `load_workspace_dependencies`.

## Visual Rules

The GitHub weekly hot image mode uses a locked template:

- cover top-right badge: `Top10 榜单`;
- cover has no `github.com` link bar;
- cover bottom icon uses a GitHub cat / Octocat-style mascot;
- detail top-left header: `GitHub 本周爆火热榜`;
- detail top-right badge: `热榜第N名`;
- trend metric shows only `+数字`, never `本周`;
- icons follow the page accent color, especially fork and trend icons;
- final cards must be 3:4.

## Example Case

See [examples/github-weekly-hot-case.md](examples/github-weekly-hot-case.md) for a real run based on GitHub Trending weekly.

## License

MIT
