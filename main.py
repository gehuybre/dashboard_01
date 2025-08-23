# Macros for downloads, metadata, embed snippets, and asset helpers
# Loaded by mkdocs-macros-plugin. Keep logic here thin and import from /macros/* for modularity.
from macros.downloads import render_download_buttons, embed_snippet, today
from macros.metadata import render_report_meta
from macros.assets import asset_page_content, embed_page_content

def define_env(env):
    # Get site URL from MkDocs config for absolute URL generation
    site_url = (env.conf.get("site_url") or "").rstrip("/")
    
    # Create site-aware wrapper functions
    def _asset_page_content(meta):
        return asset_page_content(meta, site_url)
    
    def _embed_page_content(meta):
        return embed_page_content(meta, site_url)
    
    def _embed_snippet(slug, width=800, height=480):
        return embed_snippet(slug, width, height, site_url)
    
    # Jinja macros exposed to Markdown
    env.macro(render_report_meta)
    env.macro(render_download_buttons)
    env.macro(_embed_snippet, "embed_snippet")
    env.macro(today)
    env.macro(_asset_page_content, "asset_page_content")
    env.macro(_embed_page_content, "embed_page_content")
