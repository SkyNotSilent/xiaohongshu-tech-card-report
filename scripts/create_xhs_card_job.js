#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function arg(name, fallback = "") {
  const index = process.argv.indexOf(`--${name}`);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function todayShanghai() {
  const formatter = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
  return formatter.format(new Date()).replaceAll("-", "");
}

function slugify(value) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64) || "tech-report";
}

const root = path.resolve(arg("root", process.cwd()));
const topic = slugify(arg("topic", "tech-report"));
const date = arg("date", todayShanghai());
const jobDir = path.join(root, "05_jobs", `${date}-${topic}-xhs-cards`);

const files = {
  "00_source/sources.md": "# Sources\n\n| Item | Source | Date | URL | Verified fact used |\n| --- | --- | --- | --- | --- |\n",
  "00_source/github-weekly.json": "{\n  \"repositories\": []\n}\n",
  "01_analysis/selection.md": "# Selection\n\n## Editorial angle\n\n## Selected items\n\n## Discarded or downgraded candidates\n\n",
  "02_cards/cards.md": "# Cards\n\n",
  "02_cards/xhs_caption.md": "# Xiaohongshu Caption\n\n## Title options\n\n1. \n2. \n3. \n\n## Caption\n\n## Hashtags\n\n## Comment prompt\n\n",
  "02_cards/visual_prompts.md": "# Visual Prompts\n\n",
  "02_cards/visual_prompts.json": "{\n  \"cards\": []\n}\n",
  "03_images/.gitkeep": "",
  "manifest.json": "{\n  \"status\": \"draft\",\n  \"deliverables\": []\n}\n"
};

for (const [relativePath, content] of Object.entries(files)) {
  const target = path.join(jobDir, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  if (!fs.existsSync(target)) {
    fs.writeFileSync(target, content);
  }
}

console.log(jobDir);
