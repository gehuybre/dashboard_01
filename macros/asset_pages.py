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