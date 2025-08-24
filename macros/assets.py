import os, io, json, textwrap
from datetime import date

def define_env(env):
    """Define macros for MkDocs"""
    site_url = (env.conf.get("site_url") or "").rstrip("/")  # e.g. https://gehuybre.github.io/dashboard_01

    def abs_url(path: str) -> str:
        """Convert a relative path to an absolute URL using site_url"""
        if path.startswith(("http://","https://")):
            return path
        return f"{site_url}/{path.lstrip('/')}"

    @env.macro
    def embed_iframe(slug, width=800, height=480, title=None):
        """Render a LIVE iframe to the generated -embed page with auto-height."""
        title = title or slug
        return (
            f'<iframe src="{abs_url(f"assets/{slug}-embed/")}" '
            f'width="100%" height="{height}" loading="lazy" title="{title}" '
            f'style="border:0;" data-embed-autoheight data-embed-slug="{slug}"></iframe>'
        )

    @env.macro
    def asset_page_content(meta):
        return asset_page_content_standalone(meta, site_url)
    
    @env.macro  
    def embed_page_content(meta):
        return embed_page_content_standalone(meta, site_url)

def abs_url_standalone(path: str, site_url: str) -> str:
    """Convert a relative path to an absolute URL using site_url (standalone version)"""
    if path.startswith(("http://", "https://")):
        return path
    return f"{site_url.rstrip('/')}/{path.lstrip('/')}"

def _downloads_html(files, site_url=""):
    parts = []
    mapping = {'csv':'CSV','xlsx':'XLSX','png':'PNG','svg':'SVG','html':'HTML'}
    for ext,label in mapping.items():
        if ext in files:
            # Use relative path for same-directory files - extract just the filename
            file_path = files[ext]
            if file_path.startswith('assets/'):
                file_path = file_path.split('/')[-1]  # Get just the filename
            
            # For HTML files, open in new tab; others download
            if ext == 'html':
                href = abs_url_standalone(file_path, site_url) if site_url else file_path
                parts.append(f'<a class="dl-btn" target="_blank" rel="noopener" href="{href}">{label}</a>')
            else:
                parts.append(f'<a class="dl-btn" href="{file_path}" download>{label}</a>')
    return " ".join(parts)

def asset_page_content_standalone(meta, site_url=""):
    """ Generate the main content for an asset detail page """
    from pathlib import Path
    import yaml
    
    # Extract values from meta dict
    slug = meta.get('slug')
    title = meta.get('title', slug)
    summary = meta.get('summary','')
    files = meta.get('files',{})
    atype = meta.get('type','asset')
    body = []
    
    # Interactive HTML chart takes priority
    if 'html' in files:
        # Use absolute URL for iframe for consistency
        html_path = files["html"]
        if site_url and html_path.startswith('assets/'):
            # Convert to absolute URL
            chart_url = abs_url_standalone(html_path, site_url)
        elif html_path.startswith('assets/'):
            # Extract filename from assets/slug/filename.html for relative fallback
            chart_url = html_path.split('/')[-1]
        else:
            chart_url = html_path
        body.append(f'<div class="chart-embed"><iframe src="{chart_url}" loading="lazy" allowfullscreen style="width:100%;height:600px;border:1px solid #ddd;border-radius:4px;"></iframe></div>')
    elif atype == 'figure':
        # Prefer SVG if present for crispness
        img = files.get('svg') or files.get('png')
        if img:
            # Use absolute URL for images for consistency
            img_path = img
            if site_url and img_path.startswith('assets/'):
                # Convert to absolute URL
                img_url = abs_url_standalone(img_path, site_url)
            elif img_path.startswith('assets/'):
                # Extract filename for relative fallback
                img_url = img_path.split('/')[-1]
            else:
                img_url = img_path
            body.append(f'<p><img alt="{title}" src="{img_url}"/></p>')
    
    body.append(f'<div class="download-buttons">{_downloads_html(files, site_url)}</div>')
    
    # Embed snippet using absolute URLs
    body.append('<h3>Embed</h3>')
    base_url = site_url or ""
    target = f"assets/{slug}-embed/"
    embed_url = abs_url_standalone(target, site_url) if site_url else target
    body.append(f'<pre><code>&lt;iframe src="{embed_url}" width="800" height="480" loading="lazy"&gt;&lt;/iframe&gt;</code></pre>')
    return "\n".join(body)

def embed_page_content_standalone(meta, site_url=""):
    """ Generate the content for an asset embed page with auto-height functionality """
    files = meta.get('files',{})
    title = meta.get('title', meta.get('slug', 'Asset'))
    slug = meta.get('slug', '')
    
    if 'html' in files:
        # For embed pages, construct the correct relative path to the chart
        html_path = files["html"]
        if html_path.startswith('assets/'):
            # Convert assets/slug/filename.html to ../slug/filename.html for embed pages
            path_parts = html_path.split('/')
            relative_url = f"../{'/'.join(path_parts[1:])}"  # Remove 'assets' and add '..'
        else:
            relative_url = html_path
        return f"""
<style>
  html,body {{ margin:0; padding:0; overflow:hidden; background:transparent; }}
  .chart-html {{ width:100%; border:0; min-height:560px; display:block; }}
  /* Hide theme title on *this* page only (embed pages) */
  .md-content__inner h1, .md-typeset h1 {{ display: none !important; }}
</style>
<iframe class="chart-html" src="{relative_url}" loading="eager" referrerpolicy="no-referrer"></iframe>
<script>
(function(){{
  var child = document.querySelector(".chart-html");

  function postHeight(h){{
    var H = Math.max(340, Math.ceil(h) + 24);   // increased padding for scrollbars
    child.style.height = H + "px";             // <-- make inner iframe tall enough
    document.documentElement.style.height = H + "px";
    document.body.style.height = H + "px";
    try {{ parent && parent.postMessage({{ type:"plotly-embed-size", height:H, slug:"{slug}" }}, "*"); }} catch(e) {{}}
  }}

  function measure(){{
    try {{
      var doc = child.contentDocument || child.contentWindow.document;
      if (!doc) return;
      var plot = doc.querySelector(".js-plotly-plot");
      var h = plot ? plot.getBoundingClientRect().height : Math.max(
        doc.documentElement.scrollHeight || 0,
        doc.body ? doc.body.scrollHeight : 0
      );
      if (h) postHeight(h);
    }} catch(e) {{}}
  }}

  child.addEventListener("load", function(){{
    setTimeout(measure, 80);                   // after plot renders
    try {{
      var doc = child.contentDocument || child.contentWindow.document;
      var plot = doc && doc.querySelector(".js-plotly-plot");
      if (plot && child.contentWindow && child.contentWindow.ResizeObserver) {{
        new child.contentWindow.ResizeObserver(measure).observe(plot);
      }}
    }} catch(e) {{}}
  }});
  setInterval(measure, 800);                   // safety for late re-layouts
  window.addEventListener("message", function(e) {{
    if ((e.data||{{}}).type === "plotly-embed-ping") measure();
  }});
}})();
</script>
"""
    elif 'png' in files or 'svg' in files:
        # Use relative path for images
        img_path = files.get('svg') or files.get('png')
        if img_path.startswith('assets/'):
            # Convert assets/slug/filename.ext to ../slug/filename.ext for embed pages
            path_parts = img_path.split('/')
            img_path = f"../{'/'.join(path_parts[1:])}"  # Remove 'assets' and add '..'
        return f'<img alt="{title}" src="{img_path}" style="max-width:100%;border:0;" />'
    else:
        return "<!-- no embeddable content -->"
