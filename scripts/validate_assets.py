#!/usr/bin/env python3
"""
Asset validation script for the dashboard system.

Ensures all asset.yml files follow the proper schema and reference existing files.
Run this before `mkdocs build` to catch issues early.

Usage:
    python scripts/validate_assets.py
    uv run python scripts/validate_assets.py
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_asset_yml(asset_path: Path) -> Dict[str, Any]:
    """Load and parse an asset.yml file."""
    try:
        with open(asset_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise ValueError(f"Failed to parse {asset_path}: {e}")


def validate_asset_schema(asset_data: Dict[str, Any], asset_path: Path) -> List[str]:
    """Validate asset schema and return list of errors."""
    errors = []
    
    # Required fields
    required_fields = ['slug', 'title', 'files']
    for field in required_fields:
        if field not in asset_data:
            errors.append(f"Missing required field: '{field}'")
    
    # Validate slug format (should be filesystem-safe)
    if 'slug' in asset_data:
        slug = asset_data['slug']
        if not isinstance(slug, str) or not slug.strip():
            errors.append("Field 'slug' must be a non-empty string")
        elif not slug.replace('_', '').replace('-', '').isalnum():
            errors.append(f"Field 'slug' contains invalid characters: '{slug}' (use only letters, numbers, hyphens, underscores)")
    
    # Validate files section
    if 'files' in asset_data:
        files = asset_data['files']
        if not isinstance(files, dict):
            errors.append("Field 'files' must be a dictionary")
        else:
            # If HTML file exists, validate path format
            if 'html' in files:
                html_path = files['html']
                if not isinstance(html_path, str):
                    errors.append("Field 'files.html' must be a string")
                elif not html_path.startswith('assets/'):
                    errors.append(f"Field 'files.html' must start with 'assets/' (got: '{html_path}')")
                # Note: Skipping slug path validation for new nested structure
    
    return errors


def validate_file_existence(asset_data: Dict[str, Any], docs_root: Path) -> List[str]:
    """Validate that referenced files actually exist."""
    errors = []
    
    files = asset_data.get('files', {})
    for file_type, file_path in files.items():
        if isinstance(file_path, str):
            # Convert site-rooted path to filesystem path
            if file_path.startswith('assets/'):
                fs_path = docs_root / file_path
            else:
                fs_path = docs_root / 'assets' / file_path
            
            if not fs_path.exists():
                errors.append(f"Referenced file does not exist: {file_path} (looked for: {fs_path})")
    
    return errors


def find_asset_files(docs_root: Path) -> List[Path]:
    """Find all asset.yml files in the assets directory and subdirectories."""
    assets_dir = docs_root / 'assets'
    if not assets_dir.exists():
        return []
    
    asset_files = []
    
    # Search recursively for asset.yml files
    for asset_yml in assets_dir.rglob('asset.yml'):
        asset_files.append(asset_yml)
    
    return asset_files


def main():
    """Main validation function."""
    # Find project root and docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_root = project_root / 'docs'
    
    if not docs_root.exists():
        print(f"❌ Docs directory not found: {docs_root}")
        sys.exit(1)
    
    # Find all asset.yml files
    asset_files = find_asset_files(docs_root)
    
    if not asset_files:
        print("✅ No asset.yml files found - validation passed")
        return
    
    print(f"🔍 Validating {len(asset_files)} asset file(s)...")
    
    total_errors = 0
    
    for asset_path in asset_files:
        relative_path = asset_path.relative_to(project_root)
        print(f"\n📄 Checking {relative_path}")
        
        try:
            # Load asset data
            asset_data = load_asset_yml(asset_path)
            
            # Validate schema
            schema_errors = validate_asset_schema(asset_data, asset_path)
            
            # Validate file existence
            file_errors = validate_file_existence(asset_data, docs_root)
            
            # Report errors
            all_errors = schema_errors + file_errors
            
            if all_errors:
                print(f"   ❌ {len(all_errors)} error(s):")
                for error in all_errors:
                    print(f"      • {error}")
                total_errors += len(all_errors)
            else:
                slug = asset_data.get('slug', 'unknown')
                print(f"   ✅ Valid (slug: {slug})")
        
        except Exception as e:
            print(f"   ❌ Failed to process: {e}")
            total_errors += 1
    
    # Final summary
    print(f"\n{'='*50}")
    if total_errors == 0:
        print("✅ All asset validations passed!")
        print("\n💡 Next steps:")
        print("   1. uv run python scripts/build_charts.py")
        print("   2. uv run mkdocs build --strict")
    else:
        print(f"❌ Found {total_errors} validation error(s)")
        print("\n🔧 Quick fixes:")
        print("   • Ensure 'slug' matches the directory name")
        print("   • Use 'assets/<slug>/<filename>' for all file paths")
        print("   • Make sure referenced files exist in docs/")
        sys.exit(1)


if __name__ == '__main__':
    main()
