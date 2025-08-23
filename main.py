# Macros for downloads, metadata, embed snippets, and asset helpers
# Loaded by mkdocs-macros-plugin. Keep logic here thin and import from /macros/* for modularity.
from macros.downloads import render_download_buttons, embed_snippet, today
from macros.metadata import render_report_meta
from macros.assets import asset_page_content_standalone, embed_page_content_standalone
from macros.asset_pages import embed_iframe_standalone

def define_env(env):
    # Get site URL from MkDocs config for absolute URL generation
    site_url = (env.conf.get("site_url") or "").rstrip("/")
    
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
    
    # Jinja macros exposed to Markdown
    env.macro(render_report_meta)
    env.macro(render_download_buttons)
    env.macro(_embed_snippet, "embed_snippet")
    env.macro(_embed_iframe, "embed_iframe")
    env.macro(today)
    env.macro(_asset_page_content, "asset_page_content")
    env.macro(_embed_page_content, "embed_page_content")
