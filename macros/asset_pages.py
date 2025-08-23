def define_env(env):
    """Define macros for MkDocs"""
    site_url = (env.conf.get("site_url") or "").rstrip("/")
    
    def abs_url(p): 
        return p if p.startswith(("http://","https://")) else f"{site_url}/{p.lstrip('/')}"

    @env.macro
    def embed_iframe(slug: str, width: int = 800, height: int = 480, title: str | None = None) -> str:
        """Render a LIVE iframe to the generated -embed page with auto-height."""
        title = title or slug
        url = abs_url(f"assets/{slug}-embed/")
        # Note: height here is just a starter; script will set the real height.
        return (f'<iframe src="{url}" width="100%" height="{height}" title="{title}" '
                f'loading="lazy" style="border:0;" data-embed-autoheight data-embed-slug="{slug}"></iframe>')

def embed_iframe(slug, width=800, height=480, title=None, site_url=""):
    """Render a LIVE iframe to the generated -embed page."""
    title = title or slug
    base_url = site_url or "https://gehuybre.github.io/dashboard_01"
    url = f"{base_url}/assets/{slug}-embed/"
    return f'<iframe src="{url}" width="{width}" height="{height}" loading="lazy" title="{title}" style="border:0;"></iframe>'