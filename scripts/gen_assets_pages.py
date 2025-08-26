# Generate dedicated asset pages and minimal embed pages at build time.
# Looks for /docs/assets/**/asset.yml files and emits virtual pages under /assets/.
import os, glob, yaml
import mkdocs_gen_files

DOCS = "docs"
ASSET_YMLS = glob.glob(os.path.join(DOCS, "assets", "**", "asset.yml"), recursive=True)

def write(path, content):
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)

for yml in ASSET_YMLS:
    with open(yml, "r", encoding="utf-8") as fh:
        meta = yaml.safe_load(fh) or {}
    slug = meta.get("slug")
    title = meta.get("title", slug)
    summary = meta.get("summary", "")
    tags = meta.get("tags", [])
    files = meta.get("files", {})
    
    # Organize generated pages by putting them in subdirectories
    # Legacy assets go in assets/legacy/pages/
    # Assets in /reports/ directory always go in their nested structure  
    if "legacy/" in yml:
        page_prefix = "assets/legacy/pages"
    elif "/reports/" in yml:
        # Extract report slug from path like: docs/assets/reports/vergunningen-2025/charts/nieuwbouw/
        path_parts = yml.split("/")
        if "reports" in path_parts:
            report_idx = path_parts.index("reports")
            if len(path_parts) > report_idx + 1:
                report_slug = path_parts[report_idx + 1]
                page_prefix = f"assets/reports/{report_slug}/pages"
            else:
                page_prefix = "assets/reports/pages"
        else:
            page_prefix = "assets/reports/pages"
    else:
        # Other assets go directly in assets/ for proper URL structure
        page_prefix = "assets"
    
    # Detail page
    detail_md = f"""---
title: {title}
summary: {summary}
tags: {tags}
---
# {title}

{{{{ asset_page_content({meta}) }}}}
"""
    write(f"{page_prefix}/{slug}.md", detail_md)

    # Minimal embed page  
    embed_md = f"""---
title: {title} (Embed)
embed: true
hide:
  - navigation
  - toc
---

<div data-embed="true">
{{{{ embed_page_content({meta}) }}}}
</div>
"""
    write(f"{page_prefix}/{slug}-embed.md", embed_md)
