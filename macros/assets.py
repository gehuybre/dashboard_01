import os, io, json, textwrap
from datetime import date

def abs_url(path: str, site_url: str) -> str:
    """Convert a relative path to an absolute URL using site_url"""
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
                href = abs_url(file_path, site_url) if site_url else file_path
                parts.append(f'<a class="dl-btn" target="_blank" rel="noopener" href="{href}">{label}</a>')
            else:
                parts.append(f'<a class="dl-btn" href="{file_path}" download>{label}</a>')
    return " ".join(parts)

def asset_page_content(meta, site_url=""):
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
        # Use relative path for iframe: extract just the filename
        html_path = files["html"]
        if html_path.startswith('assets/'):
            # Extract filename from assets/slug/filename.html  
            html_path = html_path.split('/')[-1]  # Get just the filename
        body.append(f'<div class="chart-embed"><iframe src="{html_path}" loading="lazy" allowfullscreen style="width:100%;height:600px;border:1px solid #ddd;border-radius:4px;"></iframe></div>')
    elif atype == 'figure':
        # Prefer SVG if present for crispness
        img = files.get('svg') or files.get('png')
        if img:
            # Use relative path for images: extract just the filename
            img_path = img
            if img_path.startswith('assets/'):
                img_path = img_path.split('/')[-1]  # Get just the filename
            body.append(f'<p><img alt="{title}" src="{img_path}"/></p>')
    
    body.append(f'<div class="download-buttons">{_downloads_html(files, site_url)}</div>')
    
    # Embed snippet using absolute URLs
    body.append('<h3>Embed</h3>')
    base_url = site_url or ""
    target = f"assets/{slug}-embed/"
    embed_url = abs_url(target, site_url) if site_url else target
    body.append(f'<pre><code>&lt;iframe src="{embed_url}" width="800" height="480" loading="lazy"&gt;&lt;/iframe&gt;</code></pre>')
    return "\n".join(body)

def embed_page_content(meta, site_url=""):
    """ Generate the content for an asset embed page (minimal, iframe-friendly) """
    files = meta.get('files',{})
    title = meta.get('title', meta.get('slug', 'Asset'))
    
    if 'html' in files:
        # Use the full path from asset.yml and convert to absolute URL
        html_path = files["html"]
        absolute_url = abs_url(html_path, site_url) if site_url else html_path
        return f'<iframe src="{absolute_url}" loading="lazy" allowfullscreen style="width:100%;height:600px;border:0;"></iframe>'
    elif 'png' in files or 'svg' in files:
        # Use the full path from asset.yml and convert to absolute URL
        img_path = files.get('svg') or files.get('png')
        absolute_url = abs_url(img_path, site_url) if site_url else img_path
        return f'<img alt="{title}" src="{absolute_url}" style="max-width:100%;height:auto;" />'
    else:
        return "<!-- no embeddable content -->"
