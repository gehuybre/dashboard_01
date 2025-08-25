#!/usr/bin/env python3
"""
Build all reports from their config.yml files.

Usage:
    python scripts/build_all_reports.py
"""

import sys
from pathlib import Path

# Add macros to path
sys.path.insert(0, str(Path(__file__).parent.parent / "macros"))

from build_report import build_report


def find_report_configs():
    """Find all report config.yml files"""
    reports_dir = Path("docs/reports")
    if not reports_dir.exists():
        return []
    
    configs = list(reports_dir.glob("*/config.yml"))
    return sorted(configs)


def build_all_reports():
    """Build all reports found in docs/reports/*/config.yml"""
    configs = find_report_configs()
    
    if not configs:
        print("📭 No report configs found in docs/reports/")
        return
    
    print(f"🏗️  Found {len(configs)} reports to build")
    
    success_count = 0
    for config_path in configs:
        try:
            print(f"\n📊 Building {config_path.parent.name}")
            build_report(str(config_path))
            success_count += 1
        except Exception as e:
            print(f"❌ Error building {config_path}: {e}")
    
    print(f"\n🎉 Built {success_count}/{len(configs)} reports successfully!")


def main():
    try:
        build_all_reports()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
