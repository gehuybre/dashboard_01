# Data Reports Site (MkDocs + GitHub Pages)

A modular, maintainable, and scalable template for publishing **data analysis reports** from VS Code + Git + GitHub.  
Write `.md` or `.ipynb`, commit, and your site auto-updates via GitHub Actions.

Features interactive chart generation with Plotly, centralized theming, and seamless asset management.

🌐 **Live Site**: https://gehuybre.github.io/dashboard_01/

## Quick start

```bash
# 1) Clone this repository
git clone https://github.com/gehuybre/dashboard_01.git
cd dashboard_01

# 2) Set up environment with uv (recommended)
uv sync

# 3) Build interactive charts (optional)
uv run python scripts/build_charts.py

# 4) Local preview
uv run mkdocs serve

# 5) GitHub Pages is already configured via GitHub Actions
#    - Just push to main branch and the site will auto-deploy
```

## Interactive Charts

This site includes a powerful chart generation system:

```bash
# Build all charts from YAML specifications
uv run python scripts/build_charts.py

# Or use the simple builder
uv run python scripts/build_charts_simple.py
```

### Add a new chart

1. **Define the chart** in `docs/_data/charts.yml`:

```yaml
charts:
  - name: my-chart
    type: line_multi
    params:
      data_path: docs/assets/my-data/data.csv
      x: date_column
      ys: ["metric1", "metric2"]
      title: "My Chart Title"
    output: docs/assets/my-data/my-chart.html
```

2. **Run the builder**: `uv run python scripts/build_charts.py`

3. **Reference in asset.yml**:

```yaml
files:
  csv: data.csv
  html: my-chart.html  # Interactive chart
```

Available chart types: `line_multi`, `bar_grouped`, `scatter_trend`, `area_filled`

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

## Attach charts/tables/assets

1. Put downloadable files under `docs/assets/<slug>/` (e.g. PNG, SVG, CSV, XLSX, HTML charts).
2. Create/edit `docs/assets/<slug>/asset.yml` to describe the asset.
3. Reference the asset from your report using the macros:

```jinja
{{ render_download_buttons({
  "slug": "your-slug",
  "title": "Your Asset Title", 
  "type": "figure",  # or "table"
  "files": { 
    "html": "assets/your-slug/chart.html",  # Interactive chart
    "png": "assets/your-slug/plot.png", 
    "csv": "assets/your-slug/data.csv"
  }
}) }}
```

**For embed snippets**:
```jinja
{{ embed_snippet("your-slug") }}
```

> The build script auto-generates **/assets/<slug>/** detail pages and **/assets/<slug>-embed/** pages with automatic iframe embedding for HTML charts.

## Theme Configuration

Customize colors, fonts, and chart appearance in `docs/_data/site.yml`:

```yaml
brand:
  name: "Your Brand"

charts:
  colors:
    primary: "#005EB8"
    secondary: "#00A3E0" 
    accent: "#FFC300"
  font_family: "Inter, system-ui, sans-serif"
  title_size: 20
  template: "simple_white"
```

All charts automatically use these theme tokens for consistency.

## Development Commands

```bash
# Install dependencies
uv sync

# Build interactive charts
uv run python scripts/build_charts.py

# Serve locally
uv run mkdocs serve

# Build static site
uv run mkdocs build

# Add new Python dependencies
uv add package-name

# Update dependencies
uv lock --upgrade
```

## Search & tags

- Full-text **search** is enabled by default.
- **Tags** are taken from each page's front matter and a tags index is exposed when using Material's `tags` plugin.

## Customize layout & CSS

- Templates live in `/templates` (Material override).  
- Global CSS is in `docs/static/css/site.css`.

## Automation

- `.ipynb` → page: just commit to `docs/reports/` (no frontend upload needed).  
- Interactive charts: define in YAML, auto-generated as HTML with Plotly.
- GitHub Actions builds on push to `main` and deploys to GitHub Pages.

## License

MIT (or your preference)
