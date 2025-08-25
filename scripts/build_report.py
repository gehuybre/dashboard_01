#!/usr/bin/env python3
"""
Per-report chart builder using config.yml approach.

Usage:
    python scripts/build_report.py docs/reports/vergunningen-2025/config.yml
"""

import yaml
import json
import hashlib
from pathlib import Path
import pandas as pd
import plotly.io as pio
import sys
import os

# Add macros to path
sys.path.insert(0, str(Path(__file__).parent.parent / "macros"))
from charts import build, load_site_config


def load_site():
    """Load site configuration"""
    return load_site_config()


def abs_out(path):
    """Ensure output path is under docs/ and create directories"""
    p = Path("docs") / Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def fingerprint(obj):
    """Create a content fingerprint for cache busting"""
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:8]


def build_report(config_path: str):
    """Build all charts for a report from its config.yml"""
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    print(f"📊 Building report from {config_path}")
    
    # Load configuration
    conf = yaml.safe_load(config_path.read_text())
    site = load_site()
    
    # Load data
    data_path = Path("docs") / conf["report"]["data"]
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    defaults = conf["report"].get("defaults", {})
    
    print(f"📈 Found {len(conf['charts'])} charts to build")
    
    # Build each chart
    for spec in conf["charts"]:
        chart_id = spec["id"]
        print(f"  Building {chart_id} ({spec['type']})")
        
        # Build the chart
        fig = build(spec["type"], df=df, site=site, spec=spec, defaults=defaults)
        
        # Save HTML to asset-slug-based directory (for validation compatibility)
        asset_slug = f'{conf["report"]["slug"]}-{chart_id}'
        asset_html_path = abs_out(f'assets/{asset_slug}/{chart_id}.html')
        pio.write_html(
            fig, 
            file=str(asset_html_path), 
            full_html=True, 
            include_plotlyjs="cdn",
            config={"responsive": True, "displaylogo": False}
        )
        
        # Also save to the reports structure for organization
        reports_html_path = abs_out(f'{conf["report"]["output_dir"]}/{chart_id}.html')
        pio.write_html(
            fig, 
            file=str(reports_html_path), 
            full_html=True, 
            include_plotlyjs="cdn",
            config={"responsive": True, "displaylogo": False}
        )
        
        # Create asset.yml for this chart
        asset = {
            "slug": f'{conf["report"]["slug"]}-{chart_id}',
            "title": spec.get("title", chart_id.replace("-", " ").title()),
            "summary": spec.get("summary", f"Interactieve grafiek – {chart_id}"),
            "tags": spec.get("tags", ["vergunningen", "Vlaanderen", "2025"]),
            "type": "interactive",
            "files": {
                "html": str(asset_html_path).replace("docs/", ""),
                "csv": conf["report"]["data"]
            }
        }
        
        # Save asset.yml
        asset_dir = abs_out(f'assets/{asset_slug}')
        asset_dir.mkdir(parents=True, exist_ok=True)
        asset_path = asset_dir / "asset.yml"
        asset_path.write_text(yaml.safe_dump(asset), encoding="utf-8")
        
        print(f"    ✅ {asset_html_path}")
        print(f"    ✅ {reports_html_path}")
        print(f"    ✅ {asset_path}")
    
    print(f"🎉 Report '{conf['report']['slug']}' built successfully!")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/build_report.py <config.yml>")
        print("Example: python scripts/build_report.py docs/reports/vergunningen-2025/config.yml")
        sys.exit(1)
    
    try:
        build_report(sys.argv[1])
    except Exception as e:
        print(f"❌ Error building report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
