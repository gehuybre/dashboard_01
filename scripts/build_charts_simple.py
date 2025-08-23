#!/usr/bin/env python3
"""
Simple chart builder - builds all charts from YAML specifications.

Usage:
    python scripts/build_charts_simple.py
"""

import yaml
import plotly.io as pio
from pathlib import Path
import sys

# Add the project root to Python path so we can import macros
sys.path.insert(0, str(Path(__file__).parent.parent))

from macros.charts import build

def main():
    """Simple chart builder following the exact specification"""
    spec_file = Path("docs/_data/charts.yml")
    
    if not spec_file.exists():
        print(f"Error: {spec_file} not found")
        return 1
    
    spec = yaml.safe_load(spec_file.read_text())
    
    for chart_spec in spec.get("charts", []):
        try:
            # Build the chart using the registry
            fig = build(chart_spec["type"], **chart_spec["params"])
            
            # Write to output path
            out = Path(chart_spec["output"])
            out.parent.mkdir(parents=True, exist_ok=True)
            pio.write_html(fig, file=out, full_html=True, include_plotlyjs='cdn')
            
            print("Wrote", out)
            
        except Exception as e:
            print(f"Error building {chart_spec.get('name', 'unknown')}: {e}")
            continue
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
