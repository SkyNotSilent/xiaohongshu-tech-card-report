# Xiaohongshu Publishing Limits

Use conservative defaults for normal Xiaohongshu image-text notes:

- title: 20 Chinese characters or fewer;
- caption body: 1000 characters or fewer;
- hashtags: 6 to 10 relevant tags.

These are operational defaults, not a guaranteed official API contract. Public platform behavior and creator tools can change. If the user requests exact current platform limits, verify again before relying on these values.

## Practical Rules

- Keep each title option short enough to display cleanly on mobile.
- Put the core hook in the title, not in a long subtitle.
- Keep the caption useful and skimmable: one short intro, 3 to 5 value bullets, one comment prompt.
- Use relevant tags only. Avoid unrelated traffic tags.
- Prefer tags such as `#GitHub`, `#开源项目`, `#程序员`, `#AI工具`, `#开发者工具`, `#效率工具`, `#技术分享`, `#小红书图文`.

## References To Recheck

- `https://www.digitaling.com/articles/757154.html`
- `https://wap.eastmoney.com/a/202507043448727835.html`
- `https://www.boutir.com/zh-my/academy/xiao-hong-shu-strategy-and-promotion-tips-and-traffic-rules`

Run:

```bash
python /Users/mima1234/.codex/skills/xiaohongshu-tech-card-report/scripts/validate_xhs_caption.py \
  02_cards/xhs_caption.md
```

before returning a publish package.
