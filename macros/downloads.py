from urllib.parse import quote
from datetime import date

def _button(label, href):
    return f'<a class="dl-btn" href="{href}" download>{label}</a>'

def _buttons_for_files(files):
    # files is a dict like {'csv': 'assets/foo/foo.csv', 'xlsx': 'assets/foo/foo.xlsx', 'html': 'assets/foo/chart.html', ...}
    order = ["html", "csv", "xlsx", "png", "svg"]
    labels = {"html":"HTML","csv":"CSV","xlsx":"XLSX","png":"PNG","svg":"SVG"}
    parts = []
    for ext in order:
        if files and ext in files:
            href = files[ext]
            parts.append(_button(labels[ext], href))
    return " ".join(parts)

def render_download_buttons(asset):
    """Render a row of download buttons for a single asset dict.
    asset: { 'slug': 'sample-plot', 'title': '...', 'files': {...} }
    """
    return f'''
<div class="download-box">
  <div class="download-title">{asset.get('title', asset.get('slug','Asset'))}</div>
  <div class="download-buttons">{_buttons_for_files(asset.get('files'))}</div>
</div>
'''.strip()

def embed_snippet(slug, width=800, height=480):
    """Return a ready-to-copy <iframe> snippet for an asset embed page."""
    # Works even if site_url isn't set; use a relative path
    src = f'assets/{slug}-embed/'
    # match Material's default content width
    return f'<iframe src="{src}" width="{int(width)}" height="{int(height)}" loading="lazy" title="{slug}"></iframe>'

def today():
    """Return today's date in a readable format."""
    return date.today().strftime("%d %B %Y")
