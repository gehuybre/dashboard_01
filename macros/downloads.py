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

def embed_snippet(slug, width=800, height=480, site_url=""):
    """Return a ready-to-copy <iframe> snippet for an asset embed page."""
    # Use the provided site_url or construct a relative URL
    if site_url:
        if not site_url.startswith(("http://","https://")):
            site_url = f"https://{site_url}"
        src = f'{site_url.rstrip("/")}/assets/{slug}-embed/'
    else:
        # Return a relative URL if no site_url provided
        src = f'assets/{slug}-embed/'
    
    # Return as a code block that users can copy
    iframe_code = f'<iframe src="{src}" width="{int(width)}" height="{int(height)}" loading="lazy" title="{slug}"></iframe>'
    return f'```html\n{iframe_code}\n```'

def today():
    """Return today's date in a readable format."""
    return date.today().strftime("%d %B %Y")
