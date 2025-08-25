#!/usr/bin/env python3
"""
Validation script for report configurations.

Usage:
    python scripts/validate_report.py docs/reports/vergunningen-2025/config.yml
"""

import yaml
import pandas as pd
from pathlib import Path
import sys
import re


def validate_report_config(config_path: str) -> bool:
    """Validate a report configuration file"""
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    print(f"🔍 Validating {config_path}")
    
    try:
        conf = yaml.safe_load(config_path.read_text())
    except Exception as e:
        print(f"❌ Invalid YAML: {e}")
        return False
    
    errors = []
    warnings = []
    
    # Check required report fields
    if "report" not in conf:
        errors.append("Missing 'report' section")
        return False
    
    report = conf["report"]
    required_fields = ["slug", "data", "output_dir"]
    for field in required_fields:
        if field not in report:
            errors.append(f"Missing required field: report.{field}")
    
    # Check data file exists and has required columns
    if "data" in report:
        data_path = Path("docs") / report["data"]
        if not data_path.exists():
            errors.append(f"Data file not found: {data_path}")
        else:
            try:
                df = pd.read_csv(data_path)
                print(f"📊 Data file has {len(df)} rows, {len(df.columns)} columns")
                
                # Check each chart has required columns
                for chart in conf.get("charts", []):
                    chart_id = chart.get("id", "unknown")
                    
                    # Check X column
                    if "x" in chart and chart["x"] not in df.columns:
                        errors.append(f"Chart '{chart_id}': X column '{chart['x']}' not found in data")
                    
                    # Check series columns
                    for series in chart.get("series", []):
                        col = series.get("column")
                        if col and col not in df.columns:
                            errors.append(f"Chart '{chart_id}': Series column '{col}' not found in data")
                            
            except Exception as e:
                errors.append(f"Error reading data file: {e}")
    
    # Check output directory is under assets/reports/
    if "output_dir" in report:
        output_dir = report["output_dir"]
        if not output_dir.startswith("assets/reports/"):
            warnings.append(f"Output directory should be under 'assets/reports/', got: {output_dir}")
    
    # Check chart configurations
    if "charts" not in conf:
        errors.append("Missing 'charts' section")
    else:
        charts = conf["charts"]
        chart_ids = set()
        
        for i, chart in enumerate(charts):
            chart_id = chart.get("id", f"chart-{i}")
            
            # Check for duplicate IDs
            if chart_id in chart_ids:
                errors.append(f"Duplicate chart ID: {chart_id}")
            chart_ids.add(chart_id)
            
            # Check required chart fields
            required_chart_fields = ["id", "type", "x", "series"]
            for field in required_chart_fields:
                if field not in chart:
                    errors.append(f"Chart '{chart_id}': Missing required field '{field}'")
            
            # Check chart type is valid
            valid_types = ["line_pair", "line_multi", "bar_grouped", "scatter_trend", "area_filled"]
            if chart.get("type") not in valid_types:
                warnings.append(f"Chart '{chart_id}': Unknown chart type '{chart.get('type')}'. Valid types: {valid_types}")
            
            # Check color aliases vs hard-coded colors
            color = chart.get("color", "")
            valid_aliases = ["primary", "secondary", "accent", "neutral", "gray"]
            if color and color not in valid_aliases:
                # Check if it looks like a hex color
                if re.match(r'^#[0-9A-Fa-f]{6}$', color):
                    warnings.append(f"Chart '{chart_id}': Hard-coded color '{color}'. Consider using color aliases: {valid_aliases}")
            
            # Check title is null (no chart titles inside figures)
            defaults = conf["report"].get("defaults", {})
            if defaults.get("title") is not None:
                warnings.append("report.defaults.title should be null (no titles inside charts)")
            
            # Check Y-axis starts at 0
            yaxis = defaults.get("yaxis", {})
            if yaxis.get("range") and yaxis["range"][0] != 0:
                warnings.append("Y-axis should start at 0 for consistency")
    
    # Report results
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print("⚠️  Validation warnings:")
        for warning in warnings:
            print(f"  • {warning}")
    
    if not errors and not warnings:
        print("✅ Configuration is valid!")
    elif not errors:
        print("✅ Configuration is valid (with warnings)")
    
    return len(errors) == 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_report.py <config.yml>")
        print("Example: python scripts/validate_report.py docs/reports/vergunningen-2025/config.yml")
        sys.exit(1)
    
    try:
        is_valid = validate_report_config(sys.argv[1])
        sys.exit(0 if is_valid else 1)
    except Exception as e:
        print(f"❌ Error validating report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
