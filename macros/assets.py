import os, io, json, textwrap
from datetime import date

def _downloads_html(files):
    parts = []
    mapping = {'csv':'CSV','xlsx':'XLSX','png':'PNG','svg':'SVG','html':'HTML'}
    for ext,label in mapping.items():
        if ext in files:
            # Use relative path - extract just the filename
            file_path = files[ext]
            if file_path.startswith('assets/'):
                file_path = file_path.split('/')[-1]  # Get just the filename
            parts.append(f'<a class="dl-btn" href="{file_path}" download>{label}</a>')
    return " ".join(parts)

def asset_page_content(meta):
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
    
    body.append(f'<div class="download-buttons">{_downloads_html(files)}</div>')
    
    # Embed snippet
    slug = meta.get('slug')
    body.append('<h3>Embed</h3>')
    body.append(f'<pre><code>&lt;iframe src="assets/{slug}-embed/" width="800" height="480" loading="lazy"&gt;&lt;/iframe&gt;</code></pre>')
    return "\n".join(body)

def embed_page_content(meta):
    """ Generate minimal content for iframe embedding """
    from pathlib import Path
    import yaml
    
    # Extract values from meta dict
    slug = meta.get('slug')
    title = meta.get('title', slug)
    files = meta.get('files',{})
    atype = meta.get('type','asset')
    
    # Interactive HTML chart takes priority for embedding
    if 'html' in files:
        # Use relative path for iframe: extract just the filename  
        html_path = files["html"]
        if html_path.startswith('assets/'):
            html_path = html_path.split('/')[-1]  # Get just the filename
        return f'<iframe src="{html_path}" loading="lazy" allowfullscreen style="width:100%;height:480px;border:0;"></iframe>'
    elif atype == 'figure':
        img = files.get('svg') or files.get('png')
        if img:
            # Use relative path for images: extract just the filename
            img_path = img
            if img_path.startswith('assets/'):
                img_path = img_path.split('/')[-1]  # Get just the filename
            return f'<img alt="{title}" src="{img_path}"/>'
    
    # fallback: simple link bundle
    links = " ".join(f'<a href="{v.split("/")[-1]}" download>{k.upper()}</a>' for k,v in files.items() if v.startswith('assets/'))
    return f'<div class="download-buttons">{links}</div>'
