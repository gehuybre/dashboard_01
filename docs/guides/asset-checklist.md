# Asset Creation Checklist

## Quick Copy/Paste Guide

When adding a new asset to your dashboard, follow this checklist to avoid common issues:

### 1. Directory Structure
```bash
docs/assets/<your-slug>/
├── asset.yml           # Required metadata file
├── data.csv           # Your data file(s)
└── chart.html         # Generated interactive chart (optional)
```

### 2. Asset.yml Template
Copy this template and customize:

```yaml
slug: your-asset-slug          # ✅ Must match directory name exactly
title: "Your Asset Title"      # ✅ Display name for the asset
summary: "Brief description"   # Optional one-line summary
tags: [tag1, tag2]            # Optional category tags  
type: "figure"                # Optional: figure, table, dataset
files:
  csv: assets/your-slug/data.csv        # ✅ Use full assets/ path
  html: assets/your-slug/chart.html     # Optional interactive chart
  png: assets/your-slug/image.png       # Optional static image
```

### 3. Common Mistakes to Avoid

❌ **Wrong slug**: slug doesn't match directory name
```yaml
# Directory: docs/assets/sales-data/
slug: sales_data  # ❌ Wrong! Should be "sales-data"
```

❌ **Relative file paths**: 
```yaml
files:
  csv: data.csv  # ❌ Wrong! Missing assets/ prefix
```

❌ **Missing files**: referencing files that don't exist
```yaml
files:
  html: assets/my-slug/chart.html  # ❌ File doesn't exist
```

### 4. Validation (Always Run This!)
```bash
# Before building, always validate your assets:
uv run python scripts/validate_assets.py

# If validation passes, build charts and site:
uv run python scripts/build_charts.py
uv run mkdocs build --strict
```

### 5. Using Assets in Reports

**Download buttons**:
```jinja
{{ render_download_buttons({
  "slug": "your-slug",
  "title": "Your Asset Title", 
  "type": "figure",
  "files": { 
    "html": "assets/your-slug/chart.html",
    "csv": "assets/your-slug/data.csv"
  }
}) }}
```

**Embedded chart**:
```jinja
{{ embed_snippet("your-slug") }}
```

### 6. Expected Results

After following this checklist, you should get:
- ✅ `/assets/your-slug/` - Detail page with download buttons
- ✅ `/assets/your-slug-embed/` - Minimal embed page for iframes
- ✅ Working interactive charts in your reports
- ✅ No 404 errors or broken links

### 7. Troubleshooting

If you see broken assets:
1. Run `uv run python scripts/validate_assets.py` 
2. Check the exact error messages
3. Fix asset.yml according to the schema above
4. Re-run the build process

**Common fixes**:
- Ensure `slug` matches directory name exactly
- Use `assets/<slug>/filename` format for all file paths
- Make sure all referenced files exist in `docs/`
