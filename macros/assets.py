import os, io, json, textwrap
from datetime import date

def _downloads_html(files):
    parts = []
    mapping = {'csv':'CSV','xlsx':'XLSX','png':'PNG','svg':'SVG'}
    for ext,label in mapping.items():
        if ext in files:
            parts.append(f'<a class="dl-btn" href="{files[ext]}" download>{label}</a>')
    return " ".join(parts)

def asset_page_content(meta):
    """Return HTML for a dedicated asset detail page."""
    title = meta.get('title', meta.get('slug','Asset'))
    summary = meta.get('summary','')
    files = meta.get('files',{})
    atype = meta.get('type','asset')
    body = []
    if atype == 'figure':
        # Prefer SVG if present for crispness
        img = files.get('svg') or files.get('png')
        if img:
            body.append(f'<p><img alt="{title}" src="/{img if not img.startswith("/") else img}"/></p>')
    body.append(f'<div class="download-buttons">{_downloads_html(files)}</div>')
    # Embed snippet
    slug = meta.get('slug')
    body.append('<h3>Embed</h3>')
    body.append(f'<pre><code>&lt;iframe src="assets/{slug}-embed/" width="800" height="480" loading="lazy"&gt;&lt;/iframe&gt;</code></pre>')
    return "\n".join(body)

def embed_page_content(meta):
    """Return minimal HTML for an embeddable page for this asset."""
    title = meta.get('title', meta.get('slug','Asset'))
    files = meta.get('files',{})
    atype = meta.get('type','asset')
    if atype == 'figure':
        img = files.get('svg') or files.get('png')
        if img:
            return f'<img alt="{title}" src="/{img if not img.startswith("/") else img}"/>'
    # fallback: simple link bundle
    links = " ".join(f'<a href="{v}" download>{k.upper()}</a>' for k,v in files.items())
    return f'<div class="download-buttons">{links}</div>'
