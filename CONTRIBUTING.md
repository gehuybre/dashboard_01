# Contributing / Content Authoring

### Naming convention
- Reports: `docs/reports/<kebab-case-title>.md` or `.ipynb`
- Assets: `docs/assets/<slug>/<slug>.<ext>`

### Required front matter
- `title`, `date` (`YYYY-MM-DD`), `author` (optional), `tags` (list), `summary`

### Add assets (download + embed)
1) Place files under `docs/assets/<slug>/`  
2) Create `asset.yml` in that folder describing the asset
3) Reference from your report with `render_download_buttons(...)` macro
4) Copy/paste the `<iframe>` embed from the asset page if needed

### Update navigation
- Edit `nav:` in `mkdocs.yml` or add awesome-nav plugin if you want directory-driven nav

### Local preview
```bash
pip install -r requirements.txt
mkdocs serve
```

### Deployment
- Pushing to `main` triggers GitHub Actions to publish the site via GitHub Pages
