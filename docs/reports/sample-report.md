---
title: Sample Analysis Report
author: Your Name
date: 2025-08-23
tags: [demo, sample, sine-wave]
summary: Small example showing how to attach assets with download buttons and embeds.
---

{{ render_report_meta() }}

## Chart

A simple sine wave chart with **PNG** and **SVG** downloads, plus an embeddable page.

{{ render_download_buttons({
  "slug": "sample-plot",
  "title": "Sine Wave Chart",
  "type": "figure",
  "files": {
    "png": "assets/sample-plot/sample-plot.png",
    "svg": "assets/sample-plot/sample-plot.svg"
  }
}) }}

**Embed:**

```
{{ embed_snippet("sample-plot") }}
```

## Table

A small data table with **CSV** and **XLSX** downloads.

{{ render_download_buttons({
  "slug": "sample-table",
  "title": "Sine Values",
  "type": "table",
  "files": {
    "csv": "assets/sample-table/sample-table.csv",
    "xlsx": "assets/sample-table/sample-table.xlsx"
  }
}) }}
