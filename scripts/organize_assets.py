#!/usr/bin/env python3
"""
Migrate assets to clean organized structure.

This script helps organize existing assets into the new clean structure:
  assets/reports/{report-slug}/charts/{chart-id}/
"""

import shutil
from pathlib import Path
import yaml

def migrate_legacy_assets():
    """Organize legacy assets into clean structure"""
    assets_dir = Path("docs/assets")
    legacy_dir = assets_dir / "legacy"
    
    # Create legacy directory if it doesn't exist
    legacy_dir.mkdir(exist_ok=True)
    
    print("🧹 Organizing legacy assets...")
    
    # Move old individual chart assets to legacy
    legacy_patterns = [
        "vergunningen-nieuwbouw",
        "vergunningen-verbouwen", 
        "vergunningen-sloop",
        "Embuild_vergunningen_story"
    ]
    
    for pattern in legacy_patterns:
        old_path = assets_dir / pattern
        if old_path.exists():
            new_path = legacy_dir / pattern
            if not new_path.exists():
                print(f"  📦 Moving {pattern} → legacy/{pattern}")
                shutil.move(str(old_path), str(new_path))
            else:
                print(f"  ⚠️  Skipping {pattern} (already in legacy)")
    
    # Move generated .md files to legacy
    md_files = list(assets_dir.glob("vergunningen-*.md"))
    if md_files:
        md_legacy_dir = legacy_dir / "generated_pages"
        md_legacy_dir.mkdir(exist_ok=True)
        for md_file in md_files:
            new_path = md_legacy_dir / md_file.name
            if not new_path.exists():
                print(f"  📄 Moving {md_file.name} → legacy/generated_pages/")
                shutil.move(str(md_file), str(new_path))

def show_current_structure():
    """Show the current assets structure"""
    assets_dir = Path("docs/assets")
    
    print("\n📂 Current assets structure:")
    print("docs/assets/")
    
    for item in sorted(assets_dir.iterdir()):
        if item.is_dir():
            print(f"  {item.name}/")
            # Show first level of subdirectories
            try:
                for subitem in sorted(item.iterdir()):
                    if subitem.is_dir():
                        print(f"    {subitem.name}/")
                    else:
                        print(f"    {subitem.name}")
            except PermissionError:
                pass
        else:
            print(f"  {item.name}")

def show_recommended_structure():
    """Show the recommended clean structure"""
    print("""
🎯 Recommended clean structure:

docs/assets/
  reports/                              # 📊 Clean per-report organization
    vergunningen-2025/
      data/
        graph_data_clean.csv            # 📈 Report-specific dataset
      charts/
        nieuwbouw/
          asset.yml                     # 📦 Chart metadata
          nieuwbouw.html               # 🎨 Interactive chart
        verbouwen/
          asset.yml
          verbouwen.html
        sloop/
          asset.yml
          sloop.html
    
    sales-analysis-2024/                # 🔮 Future reports
      data/
        sales_data.csv
      charts/
        overview/
        trends/
  
  legacy/                               # 🗂️  Backward compatibility
    vergunningen-nieuwbouw/             # Individual chart assets (old way)
    vergunningen-verbouwen/
    vergunningen-sloop/
    Embuild_vergunningen_story/         # Raw data (old location)
    generated_pages/
      vergunningen-nieuwbouw.md         # Auto-generated pages
      vergunningen-nieuwbouw-embed.md

Benefits:
✅ Report isolation: Each report owns its namespace
✅ Predictable paths: assets/reports/{slug}/charts/{chart-id}/
✅ Data co-location: Dataset lives with its charts
✅ Easy cleanup: Remove entire report folder when obsolete
✅ Clear migration: Legacy assets clearly marked
""")

def main():
    print("🏗️  Asset Organization Tool")
    print("=" * 50)
    
    show_current_structure()
    show_recommended_structure()
    
    response = input("\n❓ Migrate legacy assets to clean structure? (y/n): ").lower()
    if response == 'y':
        migrate_legacy_assets()
        print("\n✅ Migration complete!")
        show_current_structure()
        print("\n💡 Next steps:")
        print("   1. Update any hardcoded asset paths in your content")
        print("   2. Test that embedded charts still work")
        print("   3. Remove legacy/ folder when no longer needed")
    else:
        print("👋 No migration performed. Structure remains unchanged.")

if __name__ == "__main__":
    main()
