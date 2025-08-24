def define_env(env):
    """Define macros for MkDocs"""
    site_url = (env.conf.get("site_url") or "").rstrip("/")  # e.g. https://gehuybre.github.io/dashboard_01

    def abs_url(path: str) -> str:
        """Convert a relative path to an absolute URL using site_url"""
        if path.startswith(("http://","https://")):
            return path
        return f"{site_url}/{path.lstrip('/')}"

    @env.macro
    def embed_iframe(slug: str, width: int = 800, height: int = 480, title: str | None = None) -> str:
        """Render a LIVE iframe to the generated -embed page with auto-height."""
        title = title or slug
        url = abs_url(f"assets/{slug}-embed/")
        # Note: height here is just a starter; script will set the real height.
        return (f'<iframe src="{url}" width="100%" height="{height}" title="{title}" '
                f'loading="lazy" style="border:0;" data-embed-autoheight data-embed-slug="{slug}"></iframe>')

    @env.macro
    def render_download_buttons(spec):
        """Render download buttons with absolute URLs and embed code"""
        files = spec.get("files", {})
        parts = []
        
        # HTML (open in new tab, not download)
        if "html" in files:
            parts.append(f'<a class="dl-btn" href="{abs_url(files["html"])}" target="_blank" rel="noopener">HTML</a>')
        
        # CSV/XLSX (download)
        for k, label in (("csv","CSV"), ("xlsx","XLSX")):
            if k in files:
                parts.append(f'<a class="dl-btn" href="{abs_url(files[k])}" download>{label}</a>')
        
        # NEW: "download iframe code" as a small HTML file
        slug = spec.get("slug")
        if slug:
            iframe_code = f'<iframe src="{abs_url(f"assets/{slug}-embed/")}" width="800" height="480" loading="lazy" title="{slug}" style="border:0;"></iframe>'
            data_href = "data:text/html;charset=utf-8," + iframe_code.replace('"',"&quot;")
            parts.append(f'<a class="dl-btn" href="{data_href}" download="embed-{slug}.html">Embed&nbsp;code</a>')
        
        return '<div class="dl-group">' + "\n".join(parts) + "</div>"

def embed_iframe_standalone(slug, width=800, height=480, title=None, site_url=""):
    """Render a LIVE iframe to the generated -embed page (standalone version)."""
    title = title or slug
    if not site_url:
        # If no site_url provided, return a relative URL
        url = f"assets/{slug}-embed/"
    else:
        # Use absolute URL with provided site_url
        if not site_url.startswith(("http://","https://")):
            site_url = f"https://{site_url}"
        url = f"{site_url.rstrip('/')}/assets/{slug}-embed/"
    return f'<iframe src="{url}" width="{width}" height="{height}" loading="lazy" title="{title}" style="border:0;"></iframe>'