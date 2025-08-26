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
          asset.yml                     # 📦 Chart metadata (slug: reports-vergunningen-2025-charts-nieuwbouw)
          nieuwbouw.html               # 🎨 Interactive chart
        verbouwen/
          asset.yml                     # 📦 Chart metadata (slug: reports-vergunningen-2025-charts-verbouwen)
          verbouwen.html               # 🎨 Interactive chart
        sloop/
          asset.yml                     # 📦 Chart metadata (slug: reports-vergunningen-2025-charts-sloop)
          sloop.html                   # 🎨 Interactive chart
    
    sales-analysis-2024/                # 🔮 Future reports
      data/
        sales_data.csv
      charts/
        overview/
          asset.yml                     # 📦 slug: reports-sales-analysis-2024-charts-overview
          overview.html
        trends/
          asset.yml                     # 📦 slug: reports-sales-analysis-2024-charts-trends
          trends.html
  
  legacy/                               # 🗂️ Backward compatibility
    vergunningen-nieuwbouw/             # Individual chart assets (old way)
      asset.yml                         # 📦 slug: vergunningen-nieuwbouw
      nieuwbouw.html
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

### Legacy Method (Simple Structure)
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

### New Per-Report Method (Recommended)
1. Put files in the organized structure: `docs/assets/reports/{report-slug}/charts/{chart-id}/`
2. Create `docs/assets/reports/{report-slug}/charts/{chart-id}/asset.yml`
3. Use the new slug pattern in your reports:

```jinja
{{ render_download_buttons({
  "slug": "reports-{report-slug}-charts-{chart-id}",
  "title": "Your Chart Title", 
  "type": "interactive",
  "files": { 
    "html": "assets/reports/{report-slug}/charts/{chart-id}/{chart-id}.html",
    "csv": "assets/reports/{report-slug}/data/dataset.csv"
  }
}) }}
```

**Example:**
```jinja
{{ render_download_buttons({
  "slug": "reports-vergunningen-2025-charts-nieuwbouw",
  "title": "Data & grafiek – Nieuwbouw", 
  "type": "interactive",
  "files": { 
    "html": "assets/reports/vergunningen-2025/charts/nieuwbouw/nieuwbouw.html",
    "csv": "assets/reports/vergunningen-2025/data/graph_data_clean.csv"
  }
}) }}
```

**For embed iframes:**
```jinja
{{ embed_iframe("reports-vergunningen-2025-charts-nieuwbouw") }}
```

**For embed snippets:**
```jinja
{{ embed_snippet("your-slug") }}
```

> The build script auto-generates **/assets/<slug>/** detail pages and **/assets/<slug>-embed/** pages with automatic iframe embedding for HTML charts.

### Asset.yml Schema

Each asset directory must contain a valid `asset.yml` file with this structure:

#### Legacy/Simple Assets (Direct in `docs/assets/`)
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

#### New Per-Report Assets (Nested Structure)
For assets in the new `docs/assets/reports/{report-slug}/charts/{chart-id}/` structure:

```yaml
# Required fields
slug: reports-{report-slug}-charts-{chart-id}  # Reflects the nested path
title: "Your Chart Title"      # Display name
files:                         # File references
  csv: assets/reports/{report-slug}/data/dataset.csv
  html: assets/reports/{report-slug}/charts/{chart-id}/{chart-id}.html

# Optional fields  
summary: "Brief description"   # One-line summary
tags: [tag1, tag2]            # Category tags
type: "interactive"           # Type: figure, table, dataset, interactive
```

**Example for nested assets:**
```yaml
# For: docs/assets/reports/vergunningen-2025/charts/nieuwbouw/asset.yml
slug: reports-vergunningen-2025-charts-nieuwbouw
title: "Vergunningsaanvragen Nieuwbouw"
files:
  csv: assets/reports/vergunningen-2025/data/graph_data_clean.csv
  html: assets/reports/vergunningen-2025/charts/nieuwbouw/nieuwbouw.html
summary: "Interactive chart of building permits for new construction"
tags: [vergunningen, nieuwbouw, Vlaanderen]
type: "interactive"
```

**Key Rules**:
- For legacy assets: `slug` must match the directory name exactly
- For nested assets: `slug` follows pattern `reports-{report-slug}-charts-{chart-id}`
- All file paths must start with `assets/` (full path from docs root)
- Referenced files must exist in the `docs/` directory
- HTML files automatically get iframe embedding
- Asset pages are generated at `/assets/{slug}/` and `/assets/{slug}-embed/`

Run `uv run python scripts/validate_assets.py` to check for errors.

### Asset Page Generation

The system automatically generates asset detail pages and embed pages based on your `asset.yml` files:

#### Page Locations by Asset Type:
- **Legacy assets**: `assets/legacy/pages/{slug}.md` and `assets/legacy/pages/{slug}-embed.md`
- **New per-report assets**: `assets/{slug}.md` and `assets/{slug}-embed.md` (directly in assets/)
- **Other assets**: `assets/{slug}.md` and `assets/{slug}-embed.md`

#### URL Structure:
- **Detail page**: `/assets/{slug}/` (shows downloads, description)
- **Embed page**: `/assets/{slug}-embed/` (minimal iframe-friendly version)

#### Regenerating Asset Pages:
```bash
# Regenerate all asset pages after making changes
uv run python scripts/gen_assets_pages.py
```

The validation script now supports nested asset structures and validates:
- ✅ Required fields (slug, title, files)
- ✅ File path format (`assets/` prefix)
- ✅ Referenced file existence
- ✅ Slug format (alphanumeric with hyphens/underscores)

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

## Troubleshooting

### Common Asset Issues

**404 Errors on Graph Embeds:**
1. Check that asset slugs match the expected pattern:
   - Legacy: `your-asset-name` (matches directory name)
   - Per-report: `reports-{report-slug}-charts-{chart-id}`
2. Verify file paths in `asset.yml` point to actual files
3. Regenerate asset pages: `uv run python scripts/gen_assets_pages.py`
4. Rebuild site: `uv run mkdocs build --strict`

**Validation Errors:**
```bash
# Check what's wrong with your assets
uv run python scripts/validate_assets.py

# Common fixes:
# - Ensure slug uses only letters, numbers, hyphens, underscores
# - File paths must start with 'assets/'
# - Referenced files must exist in docs/ directory
```

**Asset Pages Not Generated:**
- The script recursively searches `docs/assets/` for `asset.yml` files
- Make sure your `asset.yml` files are properly formatted YAML
- Check that slugs don't contain forward slashes (use hyphens instead)

**Slug Naming Conventions:**
- Legacy assets: `my-chart-name`
- Per-report assets: `reports-my-report-charts-chart-name`
- Use hyphens to separate words, not underscores or spaces

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
