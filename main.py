# Macros for downloads, metadata, embed snippets, and asset helpers
# Loaded by mkdocs-macros-plugin. Keep logic here thin and import from /macros/* for modularity.
from macros.downloads import render_download_buttons, embed_snippet, today
from macros.metadata import render_report_meta
from macros.assets import asset_page_content_standalone, embed_page_content_standalone
from macros.asset_pages import embed_iframe_standalone

def define_env(env):
    # Get site URL from MkDocs config for absolute URL generation
    site_url = (env.conf.get("site_url") or "").rstrip("/")
    
    def abs_url(path: str) -> str:
        """Convert a relative path to an absolute URL using site_url"""
        if path.startswith(("http://","https://")):
            return path
        return f"{site_url}/{path.lstrip('/')}"
    
    # Create site-aware wrapper functions
    def _asset_page_content(meta):
        return asset_page_content_standalone(meta, site_url)
    
    def _embed_page_content(meta):
        return embed_page_content_standalone(meta, site_url)
    
    def _embed_snippet(slug, width=800, height=480):
        return embed_snippet(slug, width, height, site_url)
    
    def _embed_iframe(slug, width=800, height=480, title=None):
        # Use the new auto-sizing iframe with consistent absolute URL generation
        title = title or slug
        # Create absolute URL using site_url
        if site_url:
            url = f"{site_url}/assets/{slug}-embed/"
        else:
            url = f"assets/{slug}-embed/"
        # Note: height here is just a starter; script will set the real height.
        return (f'<iframe src="{url}" width="100%" height="{height}" title="{title}" '
                f'loading="lazy" style="border:0;" data-embed-autoheight data-embed-slug="{slug}"></iframe>')
    
    def _render_download_buttons(spec):
        """Render download buttons with absolute URLs and Flourish-style embed UI"""
        files = spec.get("files", {})
        slug  = spec.get("slug", "")
        download_parts = []
        
        # HTML (open in new tab, not download)
        if "html" in files:
            download_parts.append(f'<a class="dl-btn" href="{abs_url(files["html"])}" target="_blank" rel="noopener">HTML</a>')
        
        # CSV/XLSX/PNG/SVG (download)
        for k, label in (("csv","CSV"), ("xlsx","XLSX"), ("png","PNG"), ("svg","SVG")):
            if k in files:
                download_parts.append(f'<a class="dl-btn" href="{abs_url(files[k])}" download>{label}</a>')
        
        # Handle multiple CSV variants using csv_* naming convention
        for key in files.keys():
            if key.startswith("csv_"):
                # Extract the variant name (e.g., "csv_monthly" -> "monthly")
                variant = key[4:]  # Remove "csv_" prefix
                # Capitalize first letter for display (e.g., "monthly" -> "Monthly")
                display_name = variant.replace("_", " ").title()
                download_parts.append(f'<a class="dl-btn" href="{abs_url(files[key])}" download>CSV ({display_name})</a>')
        
        # -- Embed UI (Flourish style) - separate section ----------------------------------------
        embed_ui = ""
        if slug:
            src = abs_url(f"assets/{slug}-embed/")
            embed_ui = f"""
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
"""
        
        title = spec.get('title', spec.get('slug','Asset'))
        return f'''
<div class="download-box">
  <div class="download-title">{title}</div>
  <div class="download-buttons">{" ".join(download_parts)}</div>
  {embed_ui}
</div>
'''.strip()
    
    # Jinja macros exposed to Markdown
    env.macro(render_report_meta)
    env.macro(_render_download_buttons, "render_download_buttons")
    env.macro(_embed_snippet, "embed_snippet")
    env.macro(_embed_iframe, "embed_iframe")
    env.macro(today)
    env.macro(_asset_page_content, "asset_page_content")
    env.macro(_embed_page_content, "embed_page_content")
