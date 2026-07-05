# GitHub Weekly Hot Xiaohongshu Package

Use this reference for requests like "帮我做一个 GitHub 本周热榜的小红书图文笔记".

## Default Output

Produce a full publish package:

```text
00_source/sources.md
00_source/github-weekly.json
01_analysis/selection.md
02_cards/cards.md
02_cards/xhs_caption.md
02_cards/visual_prompts.json
03_images/01-cover.png
03_images/02-<repo>.png ... 11-<repo>.png
contact-sheet.jpg
manifest.json
clean-3x4-only.zip
```

The clean zip must contain only the 11 validated PNG files. Do not include the contact sheet, source files, old images, or non-3:4 drafts.

## Data Workflow

1. Fetch `https://github.com/trending?since=weekly`.
2. Use the first 10 repository entries as the default all-GitHub weekly Top10.
3. For each repo, verify repository metadata through the repository page or GitHub API.
4. Record:
   - rank;
   - owner/name;
   - repo URL;
   - language;
   - total stars;
   - forks;
   - `stars this week`;
   - description / README summary;
   - access date.
5. Stop instead of inventing numbers if `stars this week` is unavailable for any selected repo.

Use the active Python environment for data fetching. In Codex Desktop, prefer the bundled Python from `load_workspace_dependencies`.

```bash
python /Users/mima1234/.codex/skills/xiaohongshu-tech-card-report/scripts/fetch_github_weekly.py \
  --limit 10 \
  --out 00_source/github-weekly.json \
  --sources-md 00_source/sources.md
```

## Editorial Rules

Write each detail card around one practical judgment:

- what it is;
- why it rose this week;
- who should care;
- what workflow or decision it changes.

Avoid fake urgency and vague claims. Do not write security attack steps. For security repos, frame as learning, defense, or authorized research.

## Locked Visual System

Use built-in image generation for the actual images. Do not rebuild the card UI with HTML, SVG, Canvas, PIL, or other code.

General:

- strict 3:4 portrait cards, preferably `1086x1448`;
- premium off-white frosted glass;
- translucent rounded cards, soft bevels, subtle inner glow;
- restrained accent color per rank;
- crisp Chinese and English text;
- no watermark.

Cover card:

- filename: `01-cover.png`;
- top-left: `第 1 期`;
- top-right glass pill: crown icon + `Top10 榜单`;
- main title: `GitHub 本周爆火热榜`;
- subtitle: `本周新增星标精选 · <date range>`;
- ranking list: 10 rows with rank, repo name, progress bar, and `+数字`;
- bottom summary card only:
  - GitHub cat / Octocat-style mascot icon on the left;
  - one short issue summary;
  - optional weak `01 / 11` at bottom right;
- forbidden on cover:
  - `1/11` at top right;
  - `github.com` link bar;
  - link icon;
  - `Skill榜` or `Skill 榜单`.

Detail cards:

- filenames: `02-<repo>.png` through `11-<repo>.png`;
- top-left header: `GitHub 本周爆火热榜`;
- left/top-left issue label: `第 1 期 |`;
- top-right badge: crown icon + `热榜第N名`;
- hero: large colored rank square + repo title + Chinese subtitle;
- metric pills:
  - language;
  - total stars;
  - `+数字` only;
  - forks;
- trend metric must never include `本周`;
- fork/trend/star/language/check/link/play/crown icons must follow the page accent color, never black;
- bottom footer link may appear on detail pages only;
- bottom page number must be `02 / 11` through `11 / 11`.

## Prompt JSON Pattern

Use JSON-like prompts for image generation so constraints are explicit. Example detail prompt shape:

```json
{
  "use_case": "infographic-diagram",
  "asset_type": "xiaohongshu_3_4_carousel_detail_card",
  "page": "02 / 11",
  "canvas": {
    "ratio": "STRICT 3:4 portrait, Xiaohongshu card",
    "target": "1080x1440 style, balanced wide portrait, NOT 2:3, NOT 9:16",
    "quality": "native high-end AI poster, premium frosted glass, no code-rendered look"
  },
  "fixed_layout": {
    "top_left_title": "GitHub 本周爆火热榜",
    "issue_label": "第 1 期 |",
    "top_right_badge": "crown icon + 热榜第1名",
    "footer_page_number": "02 / 11"
  },
  "project": {
    "rank_badge": "01",
    "title": "<repo>",
    "subtitle": "<Chinese value label>",
    "accent_color": "<rank color>",
    "metric_pills": ["<language>", "<stars> Star", "+<stars_this_week>", "Forks <forks>"],
    "trend_metric_rule": "rising trend pill contains only +<stars_this_week>; DELETE 本周 completely",
    "icon_color_rule": "all icons and accent text follow the accent color; no black icons",
    "quote": "<short factual summary>",
    "insight_label": "一句话看懂",
    "insight": "<workflow A → B → C>",
    "features": ["<feature1>", "<feature2>", "<feature3>", "<feature4>"],
    "audience_title": "适合谁？",
    "audience": "<audience1> / <audience2> / <audience3>",
    "footer_link": "<repo URL without https://>"
  },
  "constraints": [
    "no Skill 榜",
    "no 本周 in trend metric",
    "no black fork icon",
    "strict 3:4",
    "crisp readable text",
    "no watermark"
  ]
}
```

## Validation

After every generated image:

Use a Python environment with Pillow installed for image validation and packaging. In Codex Desktop, call `load_workspace_dependencies` and use its bundled Python.

```bash
python /Users/mima1234/.codex/skills/xiaohongshu-tech-card-report/scripts/pack_clean_3x4.py \
  --input 03_images \
  --out clean-3x4-only.zip \
  --manifest manifest.json \
  --contact-sheet contact-sheet.jpg \
  --expected 11 \
  --fail-on-invalid
```

Use the contact sheet for manual QA. If a card has wrong text, black icons, wrong ratio, cover link bar, or `本周` in the trend metric, regenerate that card and rerun validation.
