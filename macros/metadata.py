from datetime import datetime

def _fmt_date(date):
    # Accept 'YYYY-MM-DD' or free text; default to today's date
    try:
        return datetime.fromisoformat(str(date)).strftime('%b %d, %Y')
    except Exception:
        return str(date) if date else ''

def render_report_meta(page_meta=None):
    """Render a consistent metadata header.

    Expected keys in meta: title, author, date, tags, summary
    Args:
        page_meta: Page metadata dictionary (optional, will try to get from context if not provided)
    """
    # Try to get page metadata from different sources
    meta = page_meta
    if not meta:
        # Try to access from the macro environment
        import inspect
        frame = inspect.currentframe()
        try:
            # Look through call stack for page metadata
            while frame:
                frame_locals = frame.f_locals
                if 'page' in frame_locals:
                    page = frame_locals['page']
                    if hasattr(page, 'meta'):
                        meta = page.meta
                        break
                elif 'page_meta' in frame_locals:
                    meta = frame_locals['page_meta']
                    break
                frame = frame.f_back
        finally:
            del frame
    
    if not meta:
        return "<!-- No page metadata found -->"
        
    author = meta.get('author', '')
    date = _fmt_date(meta.get('date', ''))
    tags = meta.get('tags', [])
    summary = meta.get('summary', '')
    tags_html = ""
    if isinstance(tags, (list, tuple)) and tags:
        tags_html = '<ul class="meta-tags">' + ''.join(f'<li>{t}</li>' for t in tags) + '</ul>'
    elif isinstance(tags, str) and tags.strip():
        tags_html = '<ul class="meta-tags"><li>' + tags + '</li></ul>'
    return f'''
<div class="report-meta">
  <div class="report-meta__line">
    {'<span class="report-meta__author">'+author+'</span>' if author else ''}
    {'<span class="report-meta__date">• '+date+'</span>' if date else ''}
  </div>
  {'<div class="report-meta__summary">'+summary+'</div>' if summary else ''}
  {tags_html}
</div>
'''.strip()
