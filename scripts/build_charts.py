#!/usr/bin/env python3
"""
Chart builder script - builds all charts from specifications.

Usage:
    python scripts/build_charts.py
    
This script:
1. Reads chart specifications from YAML files
2. Builds charts using the registry system
3. Outputs interactive HTML files
4. Uses smart caching to skip unchanged charts
"""

import json
import hashlib
import time
import sys
from pathlib import Path
import yaml
import plotly.io as pio

# Add the project root to Python path so we can import macros
sys.path.insert(0, str(Path(__file__).parent.parent))

from macros.charts import build

# Configuration
SPEC_PATHS = ["docs/_data/charts.yml"]  # Can be extended to support multiple spec files
CACHE_DIR = Path(".cache")
CACHE_FILE = CACHE_DIR / "charts.json"

# Ensure cache directory exists
CACHE_DIR.mkdir(exist_ok=True)

def load_cache() -> dict:
    """Load the build cache"""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_cache(cache: dict):
    """Save the build cache"""
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def fingerprint(spec_item: dict) -> str:
    """
    Generate a fingerprint for a chart specification.
    
    This includes:
    - The spec item itself (chart config)
    - Data file modification time
    - Theme file modification time
    """
    # Hash the spec item
    spec_str = json.dumps(spec_item, sort_keys=True).encode()
    h = hashlib.sha256(spec_str).hexdigest()
    
    # Include data file mtime
    data_path = Path(spec_item["data"])
    if data_path.exists():
        h += str(int(data_path.stat().st_mtime))
    else:
        print(f"Warning: Data file not found: {data_path}")
    
    # Include theme file mtime
    theme_path = Path("docs/_data/site.yml")
    if theme_path.exists():
        h += str(int(theme_path.stat().st_mtime))
    
    # Return final hash
    return hashlib.sha256(h.encode()).hexdigest()

def write_html(fig, output_path: Path):
    """Write a Plotly figure to HTML file"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write HTML with CDN-hosted Plotly.js for smaller file sizes
    pio.write_html(
        fig, 
        file=str(output_path), 
        full_html=True, 
        include_plotlyjs="cdn",
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
        }
    )

def build_all():
    """Build all charts from specifications"""
    cache = load_cache()
    changed = 0
    total = 0
    
    print("Building charts...")
    
    for spec_path in SPEC_PATHS:
        spec_file = Path(spec_path)
        if not spec_file.exists():
            print(f"Warning: Spec file not found: {spec_path}")
            continue
            
        try:
            spec = yaml.safe_load(spec_file.read_text())
        except yaml.YAMLError as e:
            print(f"Error parsing {spec_path}: {e}")
            continue
        
        charts = spec.get("charts", [])
        total += len(charts)
        
        for item in charts:
            name = item.get("name", "unnamed")
            output_path = Path(item["output"])
            
            # Generate fingerprint
            fp = fingerprint(item)
            
            # Check if we need to rebuild
            cache_key = output_path.as_posix()
            if cache.get(cache_key) == fp and output_path.exists():
                print(f"  ✓ {name} (cached)")
                continue
            
            try:
                # Build the chart
                print(f"  Building {name}...")
                fig = build(
                    chart_type=item["type"],
                    data=item["data"],
                    params=item.get("params", {})
                )
                
                # Write HTML output
                write_html(fig, output_path)
                
                # Update cache
                cache[cache_key] = fp
                changed += 1
                print(f"  ✓ {name} → {output_path}")
                
            except Exception as e:
                print(f"  ✗ Error building {name}: {e}")
                continue
    
    # Save cache
    save_cache(cache)
    
    print(f"\nSummary:")
    print(f"  Total charts: {total}")
    print(f"  Built/updated: {changed}")
    print(f"  Cached (skipped): {total - changed}")

def main():
    """Main entry point"""
    start_time = time.time()
    
    try:
        build_all()
    except KeyboardInterrupt:
        print("\nBuild interrupted by user")
        return 1
    except Exception as e:
        print(f"Build failed: {e}")
        return 1
    
    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f}s")
    return 0

if __name__ == "__main__":
    sys.exit(main())
