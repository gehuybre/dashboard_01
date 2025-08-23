# Data Reports Site (MkDocs + GitHub Pages)

A modular, maintainable, and scalable template for publishing **data analysis reports** from VS Code + Git + GitHub.  
Write `.md` or `.ipynb`, commit, and your site auto-updates via GitHub Actions.

🌐 **Live Site**: https://gehuybre.github.io/dashboard_01/

## Quick start

```bash
# 1) Clone this repository
git clone https://github.com/gehuybre/dashboard_01.git
cd dashboard_01

# 2) Set up virtual environment with uv
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml

# 3) Local preview
PYTHONPATH=/path/to/dashboard_01 mkdocs serve

# 4) GitHub Pages is already configured via GitHub Actions
#    - Just push to main branch and the site will auto-deploy
```

## Add a new report

- **Markdown**: add a file under `docs/reports/your-report.md` with front matter:

```yaml
---
title: Your Title
author: You
date: YYYY-MM-DD
tags: [tag1, tag2]
summary: One-line summary.
---
```

- **Notebook**: drop `your-report.ipynb` into `docs/reports/`. It's rendered by the `mkdocs-jupyter` plugin.

## Attach charts/tables

1. Put downloadable files under `docs/assets/<slug>/` (e.g. PNG, SVG, CSV, XLSX).
2. Create/edit `docs/assets/<slug>/asset.yml` to describe the asset.
3. Reference the asset from your report using the macros:

```jinja
{{ render_download_buttons({
  "slug": "your-slug",
  "title": "Your Asset Title",
  "type": "figure",  # or "table"
  "files": { "png": "assets/your-slug/plot.png", "svg": "assets/your-slug/plot.svg" }
}) }}
```

> The build script auto-generates **/assets/<slug>/** detail pages and **/assets/<slug>-embed/** pages.

## Search & tags

- Full-text **search** is enabled by default.
- **Tags** are taken from each page's front matter and a tags index is exposed when using Material's `tags` plugin.

## Customize layout & CSS

- Templates live in `/templates` (Material override).  
- Global CSS is in `docs/static/css/site.css`.

## Automation

- `.ipynb` → page: just commit to `docs/reports/` (no frontend upload needed).  
- GitHub Actions builds on push to `main` and deploys to GitHub Pages.

## License

MIT (or your preference)
