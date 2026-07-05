# Purple Theme GitHub Weekly Xiaohongshu Cards

Use this branch only when the user asks for a purple-themed GitHub weekly hot card set, including trigger phrases:

- `紫色 GitHub 热榜`
- `紫色主题 GitHub 热榜`
- `紫色风格 GitHub 热榜`
- `紫色的 GitHub 热榜小红书卡片`
- `紫色小红书卡片`

This branch is for text-heavy public-facing card images where repository names, ranks, star counts, forks, and weekly deltas must be exact. Prefer deterministic rendering over free-form image generation.

## Output

Default output is:

```text
00_source/sources.md
00_source/github-weekly.json
01_analysis/selection.md
02_cards/cards.md
02_cards/xhs_caption.md
03_images/01-cover.png
03_images/02-<rank-01>.png ... 11-<rank-10>.png
contact-sheet.jpg or contact-sheet.png
manifest.json
clean-3x4-only.zip
```

For preview requests, generate only 2-3 representative images first:

- cover;
- rank #1 detail;
- one mid-list detail such as rank #5 or #6.

Do not overwrite a previous full package when the user only asks to "先看看".

## Data Workflow

1. Fetch the current page from `https://github.com/trending?since=weekly`.
2. Use the first 10 repositories exactly in page order unless the user explicitly asks for filtering.
3. Record for each repository:
   - rank;
   - owner/name;
   - GitHub URL;
   - language;
   - total stars;
   - forks;
   - `stars this week`;
   - GitHub page description;
   - README or API summary when needed;
   - access date.
4. Stop rather than guess if `stars this week` is missing.
5. Refresh the data again when the current date changes or the user says "本周", "最新", "今天", or "现在".

Use the existing fetch script where possible:

```bash
python /Users/mima1234/.codex/skills/xiaohongshu-tech-card-report/scripts/fetch_github_weekly.py \
  --limit 10 \
  --out 00_source/github-weekly.json \
  --sources-md 00_source/sources.md
```

## Rendering Strategy

For this branch, deterministic rendering is preferred:

- Use HTML/CSS + Playwright screenshot, SVG, Canvas, or another precise renderer.
- Do not rely on generative image tools for final text-heavy cards.
- If using image generation for backgrounds only, composite exact text and numbers afterward with code.

Rationale: the cards contain many exact values. Free-form image generation can distort repo names, page numbers, stars, forks, and weekly deltas.

## Visual System

Core look:

- premium dark purple / graphite / black-purple background;
- restrained smoke-purple and deep rose accents;
- no cheap bright blue;
- frosted glass main card with translucent off-white fill;
- subtle 1px glass border, soft inner highlight, soft outer shadow;
- light noise or fine texture for glass, not obvious decorative blobs;
- grid background can be present but must be very low contrast;
- typography is dense, editorial, and readable on mobile.

Recommended palette:

```text
background: #07050a, #160d19, #220923
dark glass block: rgba(24,18,38,.96), rgba(57,27,72,.94), rgba(91,33,69,.92)
accent purple: #8a35d9
accent rose: #d42b8a or #e93c96
text black: #080a12, #111420
secondary text: #5b6170, #646878
glass white: rgba(255,255,255,.70-.86)
```

Avoid:

- saturated electric blue as a primary accent;
- one-note neon purple everywhere;
- pure solid white cards with no glass depth;
- heavy black shadows;
- cartoonish icons or emoji clutter;
- visible instruction text like "按 GitHub 当前顺序整理".

## Cover Layout

The cover should be public-facing, not an explanation to the user.

Required cover content:

- top-left: `GitHub 本周爆火热榜`;
- top-right: `Top10 榜单`;
- main title: `GitHub 本周 TOP 10 开源项目`;
- public-facing subtitle, for example:
  - `本周 GitHub 热榜更新：10 个高增长开源项目一次看懂。`
  - `从 AI Agent 到开发者工具，本周值得关注的开源项目都在这里。`
- one short trend summary card;
- ranked list with 10 rows, strict #1 to #10 order;
- each row should show rank, short repo name, Chinese label, language, and `+数字`.

Forbidden on cover:

- `github.com` link bar;
- top-right page number like `1/11`;
- internal process language such as `按当前顺序整理`, `严格排序`, `render rank`, `select projects`;
- `Skill榜`.

## Detail Layout

Each detail card should look like a high-end version of a compact public explainer card.

Required detail content:

- top-left: `GitHub 本周爆火热榜`;
- top-right: `热榜第N名`;
- large rank block: `01`, `02`, etc.;
- repo short name;
- Chinese value title;
- metric pills:
  - language;
  - `<total stars> Star`;
  - `+<stars this week>` only, no `本周`;
  - `Forks <forks>`;
- concise project description;
- dark glass "一句话看懂" block;
- 3-4 short feature/value points;
- `适合谁？` audience block;
- bottom detail footer may include `github.com/<owner>/<repo>` and page number `02 / 11` through `11 / 11`.

Security repos:

- Use defense/authorized framing.
- Include wording such as `授权场景`, `防御侧`, or `上线前检查`.
- Do not provide attack steps.

## Copy Rules

Write as an external publisher, not as an assistant explaining the process to the user.

Good:

- `本周 GitHub 热榜更新：10 个高增长开源项目一次看懂。`
- `一句话看懂：AI 写代码变快后，安全检测也要跟上速度。`
- `适合安全团队、后端开发者、应用上线前检查负责人。`

Bad:

- `按 GitHub Trending Weekly 当前顺序整理，从 #1 到 #10 严格排序。`
- `我帮你整理了...`
- `这个卡片用于...`
- `render rank #1 to #10`

## QA Checklist

Before delivery:

- Re-open the latest `github-weekly.json` or parsed source and compare every card's rank, repo, stars, forks, and weekly delta.
- Inspect the contact sheet.
- Inspect at least cover, #1 detail, and one long-name detail at full size.
- Check there is no old wording:
  - `Skill榜`
  - `当前顺序整理`
  - `严格排序`
  - `render`
  - `select projects`
  - `本周` inside the trend metric pill
- Check no cover link bar.
- Check text does not overlap and long repo names are truncated only in footers, not in titles unless necessary.
- Confirm all final images are 3:4 portrait.

When packaging, use `pack_clean_3x4.py` and include only final valid images in the clean zip.
