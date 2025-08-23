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
    # Detail page
    detail_md = f"""---
title: {title}
summary: {summary}
tags: {tags}
---
# {title}

{{{{ asset_page_content({meta}) }}}}
"""
    write(f"assets/{slug}.md", detail_md)

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
    write(f"assets/{slug}-embed.md", embed_md)
