# Creative Image-Generation GitHub Weekly Cards

Use this branch when the user explicitly asks for a different theme or visual direction, including:

- `换一个主题`
- `另一个主题`
- `换个风格`
- `参考这个风格`
- `按这个参考图做`
- `自由生图`
- `先生成一张首页图`

This branch takes precedence over the purple data-accurate branch, even when the user also requests a purple palette.

## Required Execution

1. Use the built-in image generation tool for every final card image.
2. Do not substitute HTML, CSS, SVG, Canvas, Playwright screenshots, or another code-rendered layout for the final image.
3. Treat supplied images as visual references. State their role in the prompt: style, composition, typography mood, or palette.
4. For a preview request, generate only the requested page. For `先生成一张首页图`, generate only the cover.
5. Include exact verified title, rank labels, repository names, and metrics in the image prompt. Inspect the result at full size. If any public-facing text or number is wrong, regenerate rather than silently correcting it with a code overlay.

## Creative Direction

- Preserve the verified GitHub Trending Weekly Top10 order and current facts.
- The user may choose any visual direction. Do not inherit the dark-purple frosted layout unless it is explicitly requested.
- Make the card feel editorial and designed, not like a generic dashboard: create a clear visual hierarchy, deliberate spacing, and a recognisable cover composition.
- Avoid bright blue as a dominant accent unless the reference specifically uses it.
- Keep cover copy public-facing. Never include production instructions, ranking-method explanations, or assistant-facing phrases.

## Cover Requirements

- top-left: `GitHub 本周爆火热榜`;
- top-right: `Top10 榜单`;
- primary title: `GitHub 本周 TOP 10 开源项目`;
- subtitle: `Top10 · 本周新增星标精选 · YYYY.MM.DD`, using the current Asia/Shanghai generation date, for example `Top10 · 本周新增星标精选 · 2026.07.10`;
- do not use a date range on the cover;
- the ranked Top10 list, in verified order, with repository short name and weekly growth;
- no GitHub URL bar and no page number in the cover header.

## Prompt Skeleton

```text
Use case: ui-mockup
Asset type: Xiaohongshu 3:4 portrait cover card
Input images: <reference image>: style and composition reference
Primary request: Create a high-end editorial cover for GitHub weekly trending open-source projects.
Visual direction: <describe only the selected reference direction>
Exact text and data: <paste verified title, subtitle, ranks, repo names, labels, and deltas>
Typography: Chinese editorial display typography, mobile-readable, no misspellings.
Avoid: dashboards, bright-blue default tech gradient, assistant-facing copy, URL bars, page number in header, distorted letters or numbers.
```
