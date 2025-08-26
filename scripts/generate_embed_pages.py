#!/usr/bin/env python3
"""
Generate embed pages for all charts from their asset.yml files.

This script creates the docs/assets/<chart-slug>-embed/index.md files automatically
from the asset.yml metadata. Run this before MkDocs build to ensure all embed pages
are up to date.
"""

from pathlib import Path, PurePosixPath
import yaml
import sys

def generate_embed_pages():
    """Generate embed pages for all chart assets."""
    
    docs_dir = Path("docs")
    assets_dir = docs_dir / "assets"
    
    if not assets_dir.exists():
        print("ERROR: docs/assets directory not found")
        sys.exit(1)
    
    generated_count = 0
    errors = []
    
    # Find all asset.yml files in direct subdirectories of assets/
    for asset_yml in assets_dir.glob("*/asset.yml"):
        try:
            slug = asset_yml.parent.name
            
            # Skip if this is already an embed folder
            if slug.endswith("-embed"):
                continue
                
            # Load asset metadata
            data = yaml.safe_load(asset_yml.read_text(encoding="utf-8"))
            
            title = data.get("title", slug)
            html_path = data["files"]["html"]
            
            # Create embed directory
            embed_dir = assets_dir / f"{slug}-embed"
            embed_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate embed page content
            embed_content = f"""# {title} (Embed)

{{% raw %}}<iframe src="/{html_path}" width="100%" height="560" loading="lazy" style="border:0;"></iframe>{{% endraw %}}
"""
            
            # Write embed page
            embed_page = embed_dir / "index.md"
            embed_page.write_text(embed_content, encoding="utf-8")
            
            print(f"Generated embed page: {embed_page.relative_to(docs_dir)}")
            generated_count += 1
            
        except Exception as e:
            errors.append(f"Error processing {asset_yml}: {e}")
    
    # Report results
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)
    
    print(f"Successfully generated {generated_count} embed pages")

if __name__ == "__main__":
    generate_embed_pages()
