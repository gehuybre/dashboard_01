# Macros for downloads, metadata, embed snippets, and asset helpers
# Loaded by mkdocs-macros-plugin. Keep logic here thin and import from /macros/* for modularity.
from macros.downloads import render_download_buttons, embed_snippet, today
from macros.metadata import render_report_meta
from macros.assets import asset_page_content, embed_page_content

def define_env(env):
    # Jinja macros exposed to Markdown
    env.macro(render_report_meta)
    env.macro(render_download_buttons)
    env.macro(embed_snippet)
    env.macro(today)
    env.macro(asset_page_content)
    env.macro(embed_page_content)
