---
name: xiaohongshu-tech-card-report
description: Produce Xiaohongshu carousel card reports and publish packages for GitHub weekly hotspots, GitHub 本周热榜的小红书图文笔记, GitHub Trending weekly Top10, purple-themed GitHub weekly hot cards, AI daily reports, AI news digests, tech tool roundups, and one-card-per-item social posts. Use this whenever the user asks for GitHub 每周热点, GitHub 一周热榜, GitHub 本周热榜, GitHub 热榜小红书图文笔记, 紫色 GitHub 热榜, 紫色主题 GitHub 热榜, 紫色风格 GitHub 热榜, 紫色小红书卡片, 每日 AI 日报, AI 日报, 小红书卡片, 图文卡片, carousel posts, or wants current AI/GitHub topics turned into publish-ready Xiaohongshu images, title, caption, tags, and source records. If the user asks for GitHub 热榜视频, GitHub 一周热榜视频, GitHub Trending weekly video, Remotion 视频, or a complete audio/video output, hand off to article-to-remotion-video and its GitHub weekly Remotion video reference.
---

# Xiaohongshu Tech Card Report

Use this skill to turn current GitHub or AI news into a Xiaohongshu-ready package: verified sources, card copy, visual prompts, generated carousel images when requested, and a publish caption. Every completed package must also return directly copyable titles, publish caption, and hashtags in the final response.

Default behavior for "帮我做一个 GitHub 本周热榜的小红书图文笔记": produce a full GitHub weekly hot package from GitHub Trending weekly Top10, including 1 cover + 10 detail images, a clean 3:4-only zip, title options, caption, hashtags, and source files.

## Modes

- **GitHub weekly hot XHS image mode**: For GitHub 本周热榜 / GitHub 一周热榜 / GitHub Trending weekly / GitHub 热榜小红书图文笔记. Use GitHub Trending weekly Top10 as the default ranking, then generate the full Xiaohongshu package.
- **Purple data-accurate GitHub weekly mode**: For a standard 紫色 GitHub 热榜 / 紫色主题 GitHub 热榜 / 紫色风格 GitHub 热榜 / 紫色小红书卡片 request where ranks, repository names, stars, forks, and weekly deltas must stay exact. Use the verified GitHub Trending weekly Top10 and the deterministic purple frosted-glass visual system. Read `references/github-weekly-purple-theme-xhs.md` before executing this branch.
- **Creative image-generation theme mode**: For `换一个主题`, `另一个主题`, `换个风格`, `参考这个风格`, `按这个参考图做`, `自由生图`, or `先生成一张首页图`. Use the built-in image generation tool for the final image. Read `references/github-weekly-creative-imagegen-xhs.md` before executing this branch. This branch has priority over the purple data-accurate branch whenever both could apply.
- **GitHub weekly copy-only mode**: If the user asks for 文案 / 先别生图, produce sources, cards, visual prompt JSON, and caption first.
- **Daily AI report**: For 每日 AI 日报 / 今日 AI / AI 快讯. Build a curated current-source card report.
- **Provided source mode**: If the user gives links, screenshots, markdown, or notes, use them first and verify freshness for "today", "this week", "latest", rankings, stars, launches, pricing, or product status.
- **Rewrite mode**: If the user gives an existing draft, preserve verified facts and convert it into Xiaohongshu cards.
- **Video handoff mode**: If the user asks for video, load `/Users/mima1234/.codex/skills/article-to-remotion-video/references/github-weekly-remotion-video.md` and use the video workflow instead of this card workflow.

## GitHub Weekly Hot Default Workflow

For a full GitHub weekly hot Xiaohongshu package:

1. Create a job folder with `scripts/create_xhs_card_job.js`.
2. Fetch current weekly Top10 with `scripts/fetch_github_weekly.py`.
3. Write `sources.md`, `selection.md`, `cards.md`, `visual_prompts.json`, and `xhs_caption.md`.
4. Use the built-in image generation tool for the 11 images. Do not draw the card UI with code.
5. After each image, check the pixel ratio. Discard and regenerate any image that is not 3:4.
6. Use `scripts/pack_clean_3x4.py` with a Python environment that has Pillow installed to create `clean-3x4-only.zip`. In Codex Desktop, call `load_workspace_dependencies` and use the bundled Python. The zip must contain only the 11 valid PNG images.
7. Use `scripts/validate_xhs_caption.py` before final delivery.

Read `references/github-weekly-hot-xhs.md` before executing this mode. It contains the locked visual system, output structure, prompt JSON schema, and QA rules.

Use the purple data-accurate branch only for the standard purple theme request. It intentionally uses deterministic HTML/Canvas/SVG rendering for text-heavy cards so ranks, stars, forks, and weekly deltas do not drift. When the user requests a different theme or provides a new visual reference, use the creative image-generation branch instead. Never silently replace that branch with HTML, CSS, SVG, Canvas, or a code-rendered card.

## Workspace Layout

Use the helper script when possible:

```bash
node /Users/mima1234/.codex/skills/xiaohongshu-tech-card-report/scripts/create_xhs_card_job.js \
  --root /path/to/workspace \
  --topic github-weekly-hot
```

Default job structure:

```text
05_jobs/<YYYYMMDD-topic-xhs-cards>/
  00_source/sources.md
  00_source/github-weekly.json
  01_analysis/selection.md
  02_cards/cards.md
  02_cards/xhs_caption.md
  02_cards/visual_prompts.json
  03_images/
  manifest.json
```

When working in a projectless Codex thread, put user-facing deliverables under that thread's `outputs/` directory.

## Source Rules

Freshness matters. If the post is about "today", "this week", "latest", rankings, stars, launches, model releases, pricing, company news, or tool status, verify with live sources before writing.

For GitHub weekly hot packages:

- Start from `https://github.com/trending?since=weekly`.
- Include the first 10 repositories unless the user explicitly asks for an AI/tool-filtered selection.
- Record repository URL, owner/name, language, stars, forks, stars this week, README summary, and access date.
- Do not invent star gains. If `stars this week` is missing, stop and say the source is insufficient for the default package.
- Open each repository page or GitHub API record before writing claims.
- Treat security/hacking repositories neutrally. Say "仅限授权安全研究" when relevant; do not provide operational attack steps.

For daily AI reports, prefer official blogs, release notes, docs, research papers, GitHub repos, and company announcements. Use newsletters, X posts, Product Hunt, or media articles only as discovery signals unless they are the actual source of the claim.

## Card And Caption Rules

Keep card copy scan-friendly and concrete:

- one idea per card;
- 3 bullets max when using bullet cards;
- avoid fake urgency like "全网炸了", "史诗级", "必须收藏";
- preserve English repo/product names, but explain the value in Chinese;
- every item card must answer what it is, why it is hot now, and who should care.

For Xiaohongshu caption limits, read `references/xhs-publishing-limits.md`. Default to:

- title options: 20 Chinese characters or fewer;
- caption body: 1000 characters or fewer;
- hashtags: 6 to 10 relevant tags.

For every GitHub weekly hot package, the final tag set must include these four fixed tags:

- `#GitHub`
- `#开源项目`
- `#GitHub热榜`
- `#科技资讯`

Choose the remaining 2 to 6 tags from the verified weekly topics, such as `#AI工具`, `#AI编程`, `#AIAgent`, `#开发者工具`, or `#效率工具`. Do not add unrelated traffic tags.

## Visual Rules For The Locked GitHub Template

The default and creative image-generation branches use the built-in image generation tool for actual card images. Code may only validate dimensions, create contact sheets, write manifests, and zip files. The purple data-accurate branch is the sole exception and follows its dedicated reference.

Locked GitHub weekly hot visual invariants:

- all images are strict 3:4 portrait PNGs, typically `1086x1448` or equivalent;
- cover top-right badge is `Top10 榜单`, not a page number;
- cover has no `github.com` link bar;
- cover bottom icon is a GitHub cat/Octocat-style mascot mark;
- detail top-left header is `GitHub 本周爆火热榜`;
- detail top-right badge is `热榜第N名`;
- detail footer page number is `02 / 11` through `11 / 11`;
- trend metric pill shows only `+数字`, never `本周`;
- icons and accent text follow the page primary color, especially fork and trend icons;
- never allow old wording like `Skill榜`, black fork icons, wrong page numbers, or link bars on the cover.

## Required Deliverables

For full GitHub weekly hot mode, save and return:

- `00_source/sources.md`
- `00_source/github-weekly.json`
- `01_analysis/selection.md`
- `02_cards/cards.md`
- `02_cards/xhs_caption.md`
- `02_cards/visual_prompts.json`
- `manifest.json`
- `contact-sheet.jpg` for QA preview
- `clean-3x4-only.zip` containing only valid 3:4 PNGs

If the user asks for "先给我文案", return `cards.md` and `xhs_caption.md` first, but still keep source notes durable.

## Final Delivery Format

For every completed image package, include the following directly in the final response, even when the same content is saved in `02_cards/xhs_caption.md`:

```text
标题：
<one recommended title, followed by optional alternatives>

发布文案：
<ready-to-post caption>

标签：
#GitHub #开源项目 #GitHub热榜 #科技资讯 <2-6 verified-topic tags>
```

Keep the caption externally publishable. Do not include production notes, ranking-method explanations, or instructions to the user in the publish copy.

## Quality Check

Before final response:

- Reopen generated files and check that factual claims have sources.
- Confirm date language matches the current date and source dates.
- Run `validate_xhs_caption.py` for title/body/tag limits.
- Run `pack_clean_3x4.py`; do not manually zip mixed folders.
- Inspect `contact-sheet.jpg` for visual defects before delivering.
- Report if image generation produced any discarded non-3:4 or flawed attempts.
