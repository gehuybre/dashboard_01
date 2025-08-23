#!/usr/bin/env python3
"""Create a new report skeleton (Markdown front matter) and optional asset folder."""
import argparse, os, datetime, textwrap

parser = argparse.ArgumentParser()
parser.add_argument("slug", help="kebab-case slug for your report, e.g., retail-forecast-q3")
parser.add_argument("--title", default=None)
parser.add_argument("--author", default=None)
parser.add_argument("--date", default=None, help="YYYY-MM-DD (defaults to today)")
parser.add_argument("--tags", default="", help="comma-separated")
parser.add_argument("--summary", default="")
parser.add_argument("--with-assets", action="store_true", help="create docs/assets/<slug>/")
args = parser.parse_args()

docs = "docs"
reports = os.path.join(docs, "reports")
os.makedirs(reports, exist_ok=True)

title = args.title or args.slug.replace("-", " ").title()
date = args.date or str(datetime.date.today())
tags = [t.strip() for t in args.tags.split(",") if t.strip()]

report_path = os.path.join(reports, f"{args.slug}.md")
fm = textwrap.dedent(f"""
---
title: {title}
author: {args.author or ""}
date: {date}
tags: {tags}
summary: {args.summary}
---

{{{{ render_report_meta(meta) }}}}

# {title}

Write your analysis here.
""").lstrip()

with open(report_path, "w", encoding="utf-8") as f:
    f.write(fm)

if args.with_assets:
    assets_dir = os.path.join(docs, "assets", args.slug)
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(assets_dir, "asset.yml"), "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(f"""
        slug: {args.slug}
        title: {title} (Asset)
        type: figure
        summary: Asset backing {title}
        tags: [{', '.join(tags)}]
        files: {{}}
        """).lstrip())
print("Created:", report_path)
