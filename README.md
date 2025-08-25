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

This site includes a powerful chart generation system with two approaches:

### Legacy Global Charts (charts.yml)
```bash
# Build all charts from global YAML specifications
uv run python scripts/build_charts.py

# Or use the simple builder
uv run python scripts/build_charts_simple.py
```

### New Per-Report Configuration (Recommended)
```bash
# Build one report from its config
uv run python scripts/build_report.py docs/reports/vergunningen-2025/config.yml

# Build all reports
uv run python scripts/build_all_reports.py

# Validate report configuration
uv run python scripts/validate_report.py docs/reports/vergunningen-2025/config.yml
```

### Add a new report (Per-Report Method)

1. **Create report directory**: `docs/reports/your-report/`

2. **Create config.yml**:
```yaml
report:
  slug: your-report
  data: assets/your-data/clean_dataset.csv
  output_dir: assets/reports/your-report/charts
  defaults:
    title: null  # No titles inside charts
    yaxis:
      range: [0, null]  # Y-axis starts at 0
    legend:
      orientation: h
      y: 1.05

charts:
  - id: chart-name
    type: line_pair  # or line_multi, bar_grouped, etc.
    x: date_column
    series:
      - column: monthly_data
        role: monthly
      - column: moving_average
        role: trend
    color: primary  # Uses site palette
    title: "Chart Title"
    summary: "Chart description"
```

3. **Build**: `uv run python scripts/build_report.py docs/reports/your-report/config.yml`

Available chart types: `line_pair`, `line_multi`, `bar_grouped`, `scatter_trend`, `area_filled`

### Add a chart (Legacy Global Method)

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

## Asset Organization

### Clean Structure (Recommended)

The new per-report system organizes assets in a clean, scalable structure:

```
docs/assets/
  reports/                              # 📊 Per-report organization
    vergunningen-2025/
      data/
        graph_data_clean.csv            # 📈 Report-specific dataset
      charts/
        nieuwbouw/
          asset.yml                     # 📦 Chart metadata
          nieuwbouw.html               # 🎨 Interactive chart
        verbouwen/
          asset.yml
          verbouwen.html
    
    sales-analysis-2024/                # 🔮 Future reports
      data/
        sales_data.csv
      charts/
        overview/
        trends/
  
  legacy/                               # 🗂️ Backward compatibility
    vergunningen-nieuwbouw/             # Individual chart assets (old way)
    Embuild_vergunningen_story/         # Raw data (old location)
```

**Benefits:**
- ✅ **Report isolation**: Each report owns its namespace
- ✅ **Predictable paths**: `assets/reports/{slug}/charts/{chart-id}/`
- ✅ **Data co-location**: Dataset lives with its charts
- ✅ **Easy cleanup**: Remove entire report folder when obsolete
- ✅ **Scalable**: No naming conflicts as you add reports

### Migration Tool

Organize existing assets with the migration script:

```bash
# Review current structure and migrate legacy assets
uv run python scripts/organize_assets.py
```

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

### Asset.yml Schema

Each asset directory must contain a valid `asset.yml` file with this structure:

```yaml
# Required fields
slug: your-asset-slug          # Must match directory name
title: "Your Asset Title"      # Display name
files:                         # File references
  csv: assets/your-slug/data.csv        # Use full assets/ path
  html: assets/your-slug/chart.html     # Interactive chart (optional)
  png: assets/your-slug/image.png       # Static image (optional)

# Optional fields  
summary: "Brief description"   # One-line summary
tags: [tag1, tag2]            # Category tags
type: "figure"                # Type: figure, table, dataset
```

**Key Rules**:
- `slug` must match the directory name exactly
- All file paths must start with `assets/<slug>/`
- Referenced files must exist in the `docs/` directory
- HTML files automatically get iframe embedding

Run `uv run python scripts/validate_assets.py` to check for errors.

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

# Validate asset configuration (recommended before building)
uv run python scripts/validate_assets.py

# Build interactive charts
uv run python scripts/build_charts.py

# Serve locally
uv run mkdocs serve

# Build static site (full production build)
uv run mkdocs build --strict

# Add new Python dependencies
uv add package-name

# Update dependencies
uv lock --upgrade
```

### Build Order (Important!)

For reliable builds, choose one approach:

**Per-Report Method (Recommended)**:
1. **Validate**: `uv run python scripts/validate_report.py docs/reports/<slug>/config.yml`
2. **Build charts**: `uv run python scripts/build_report.py docs/reports/<slug>/config.yml`
3. **Build site**: `uv run mkdocs build --strict`

**Legacy Global Method**:
1. **Validate assets**: `uv run python scripts/validate_assets.py`
2. **Build charts**: `uv run python scripts/build_charts.py` 
3. **Build site**: `uv run mkdocs build --strict`

This ensures asset metadata is valid before generating charts and pages.

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
