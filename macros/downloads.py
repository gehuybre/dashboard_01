from urllib.parse import quote
from datetime import date

# Legacy functions for backward compatibility
def render_download_buttons(spec: dict, site_url: str = "") -> str:
    """Legacy function - use the macro version with abs_url for proper site_url handling"""
    def abs_url(path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{site_url}/{path.lstrip('/')}" if site_url else path

    def _btn(label, href, download=False):
        if download:
            return f'<a class="dl-btn" href="{href}" download>{label}</a>'
        return f'<a class="dl-btn" href="{href}" target="_blank" rel="noopener">{label}</a>'

    files = spec.get("files", {})
    slug  = spec.get("slug", "")
    parts = []
    if "html" in files: parts.append(_btn("HTML", abs_url(files["html"]), download=False))
    if "csv"  in files: parts.append(_btn("CSV",  abs_url(files["csv"]),  download=True))
    if "xlsx" in files: parts.append(_btn("XLSX", abs_url(files["xlsx"]), download=True))
    if "png"  in files: parts.append(_btn("PNG",  abs_url(files["png"]),  download=True))
    if "svg"  in files: parts.append(_btn("SVG",  abs_url(files["svg"]),  download=True))

    # -- Embed UI (Flourish style) ----------------------------------------
    if slug:
        src = abs_url(f"assets/{slug}-embed/")
        parts.append(f"""
<div class="embed-ui" data-embed-slug="{slug}" data-embed-src="{src}">
  <div class="label-row">
    <strong>Embed on your website</strong>
    <a class="link" href="{src}" target="_blank" rel="noopener">Open embed</a>
  </div>
  <div class="code-row">
    <textarea class="embed-code" readonly></textarea>
    <button type="button" class="embed-copy">Copy</button>
  </div>
  <details>
    <summary>More options</summary>
    <div class="opts">
      <label>Width <input class="embed-width" type="number" value="800" min="200" step="10"></label>
      <label>Height <input class="embed-height" type="number" value="480" min="200" step="10"></label>
      <label><input class="embed-border" type="checkbox" checked> No border</label>
    </div>
  </details>
</div>
""")
    return '<div class="dl-group">' + "\n".join(parts) + "</div>"

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

# MkDocs macros plugin integration
def define_env(env):
    site_url = (env.conf.get("site_url") or "").rstrip("/")

    def abs_url(path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{site_url}/{path.lstrip('/')}"

    def _btn(label, href, download=False):
        if download:
            return f'<a class="dl-btn" href="{href}" download>{label}</a>'
        return f'<a class="dl-btn" href="{href}" target="_blank" rel="noopener">{label}</a>'

    @env.macro
    def render_download_buttons_macro(spec: dict) -> str:
        files = spec.get("files", {})
        slug  = spec.get("slug", "")
        parts = []
        if "html" in files: parts.append(_btn("HTML", abs_url(files["html"]), download=False))
        if "csv"  in files: parts.append(_btn("CSV",  abs_url(files["csv"]),  download=True))
        if "xlsx" in files: parts.append(_btn("XLSX", abs_url(files["xlsx"]), download=True))
        if "png"  in files: parts.append(_btn("PNG",  abs_url(files["png"]),  download=True))
        if "svg"  in files: parts.append(_btn("SVG",  abs_url(files["svg"]),  download=True))

        # -- Embed UI (Flourish style) ----------------------------------------
        if slug:
            src = abs_url(f"assets/{slug}-embed/")
            parts.append(f"""
<div class="embed-ui" data-embed-slug="{slug}" data-embed-src="{src}">
  <div class="label-row">
    <strong>Embed on your website</strong>
    <a class="link" href="{src}" target="_blank" rel="noopener">Open embed</a>
  </div>
  <div class="code-row">
    <textarea class="embed-code" readonly></textarea>
    <button type="button" class="embed-copy">Copy</button>
  </div>
  <details>
    <summary>More options</summary>
    <div class="opts">
      <label>Width <input class="embed-width" type="number" value="800" min="200" step="10"></label>
      <label>Height <input class="embed-height" type="number" value="480" min="200" step="10"></label>
      <label><input class="embed-border" type="checkbox" checked> No border</label>
    </div>
  </details>
</div>
""")
        return '<div class="dl-group">' + "\n".join(parts) + "</div>"

    @env.macro
    def embed_snippet_macro(slug, width=800, height=480):
        """Return a ready-to-copy <iframe> snippet for an asset embed page."""
        src = abs_url(f"assets/{slug}-embed/")
        iframe_code = f'<iframe src="{src}" width="{int(width)}" height="{int(height)}" loading="lazy" title="{slug}"></iframe>'
        return f'```html\n{iframe_code}\n```'

    @env.macro
    def today_macro():
        """Return today's date in a readable format."""
        return date.today().strftime("%d %B %Y")
