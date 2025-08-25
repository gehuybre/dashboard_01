# Chart registry and theme system
from dataclasses import dataclass
from typing import Callable, Dict
from pathlib import Path
import yaml
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Global registry for chart types
_REGISTRY: Dict[str, Callable] = {}

def chart(name: str):
    """Decorator to register chart builder functions"""
    def wrap(fn): 
        _REGISTRY[name] = fn
        return fn
    return wrap

@dataclass
class Theme:
    """Theme configuration for charts"""
    colors: list
    template: str
    font: str
    title_size: int

def load_theme() -> Theme:
    """Load theme configuration from site.yml"""
    site_path = Path("docs/_data/site.yml")
    if not site_path.exists():
        # Fallback theme if site.yml doesn't exist
        return Theme(
            colors=["#005EB8", "#00A3E0", "#FFC300"],
            template="simple_white",
            font="Inter, sans-serif",
            title_size=20
        )
    
    site = yaml.safe_load(site_path.read_text())
    c = site["charts"]["colors"]
    charts_config = site["charts"]
    
    return Theme(
        colors=[c["primary"], c["secondary"], c["accent"]],
        template=charts_config.get("template", "simple_white"),
        font=charts_config["font_family"],
        title_size=charts_config["title_size"]
    )

def load_site_config():
    """Load full site configuration"""
    site_path = Path("docs/_data/site.yml")
    if site_path.exists():
        return yaml.safe_load(site_path.read_text())
    return {}

def color_from_alias(alias: str, site: dict) -> str:
    """Resolve color alias to actual color value"""
    if not isinstance(alias, str):
        return alias  # Already a color value
    
    colors = site.get("charts", {}).get("colors", {})
    color_map = {
        "primary": colors.get("primary", "#005EB8"),
        "secondary": colors.get("secondary", "#00A3E0"), 
        "accent": colors.get("accent", "#FFC300"),
        "neutral": colors.get("neutral", "#5F6A6A"),
        "gray": colors.get("gray", "#D5D8DC")
    }
    return color_map.get(alias, alias)

def apply_theme_and_responsive(fig, theme: Theme):
    """Apply theme and responsive settings to a figure"""
    fig.update_layout(
        template=theme.template,
        colorway=theme.colors,
        font=dict(family=theme.font),
        title_font_size=theme.title_size,
        # Responsive margins and sizing
        margin=dict(l=40, r=10, t=40, b=40),
        autosize=True,
        # Remove "variable" from legend title
        legend=dict(title_text="")
    )
    
    # Y starts at 0
    fig.update_yaxes(range=[0, None], ticks="outside", zeroline=True, zerolinewidth=1)
    
    # X shows quarters
    fig.update_xaxes(
        dtick="M3",                 # one tick every 3 months
        tickformat="%b %Y",         # shows Jan/Apr/Jul/Oct
        ticks="outside"
    )
    
    return fig

@chart("line_multi")
def line_multi(data_path, x, ys, title):
    """Multi-line chart builder"""
    theme = load_theme()
    df = pd.read_csv(data_path)
    
    fig = px.line(df, x=x, y=ys, title=title)
    
    # Apply theme and responsive settings
    apply_theme_and_responsive(fig, theme)
    
    # Style traces and clean up hover template
    fig.update_traces(
        line=dict(width=2),
        hovertemplate="%{fullData.name}<br>%{xaxis.title.text}=%{x}<br>%{yaxis.title.text}=%{y}<extra></extra>"
    )
    
    return fig

@chart("bar_grouped")
def bar_grouped(data_path, x, y, color, title):
    """Grouped bar chart builder"""
    theme = load_theme()
    df = pd.read_csv(data_path)
    
    fig = px.bar(df, x=x, y=y, color=color, title=title, barmode='group')
    
    # Apply theme and responsive settings
    apply_theme_and_responsive(fig, theme)
    
    return fig

@chart("scatter_trend")
def scatter_trend(data_path, x, y, color=None, title="", trendline=True):
    """Scatter plot with trend line"""
    theme = load_theme()
    df = pd.read_csv(data_path)
    
    fig = px.scatter(
        df, x=x, y=y, color=color, title=title,
        trendline="ols" if trendline else None
    )
    
    # Apply theme and responsive settings
    apply_theme_and_responsive(fig, theme)
    
    return fig

@chart("area_filled")
def area_filled(data_path, x, y, color=None, title=""):
    """Area chart builder"""
    theme = load_theme()
    df = pd.read_csv(data_path)
    
    fig = px.area(df, x=x, y=y, color=color, title=title)
    
    # Apply theme and responsive settings
    apply_theme_and_responsive(fig, theme)
    
    return fig

@chart("line_pair")
def line_pair(df: pd.DataFrame, site: dict, spec: dict, defaults: dict):
    """Line chart with monthly data + trend line (dashed + solid)"""
    # Resolve color
    color = spec.get("color", "primary")
    if color in ("primary", "secondary", "accent", "neutral", "gray"):
        color = color_from_alias(color, site)

    x = spec["x"]
    monthly_series = next(s for s in spec["series"] if s["role"] == "monthly")
    trend_series = next(s for s in spec["series"] if s["role"] == "trend")
    
    monthly_col = monthly_series["column"]
    trend_col = trend_series["column"]

    fig = go.Figure([
        go.Scatter(
            x=df[x], y=df[monthly_col], 
            mode="lines",
            name="Maandelijks niveau", 
            line=dict(color=color, width=2, dash="dash")
        ),
        go.Scatter(
            x=df[x], y=df[trend_col], 
            mode="lines",
            name="1-jarig voortschrijdend gemiddelde", 
            line=dict(color=color, width=3)
        ),
    ])

    # Merge defaults for axes/legend
    y_cfg = defaults.get("yaxis", {})
    fig.update_yaxes(
        range=y_cfg.get("range", [0, None]), 
        automargin=True, 
        ticks="outside",
        zeroline=True,
        zerolinewidth=1
    )

    x_cfg = spec.get("xaxis", {})
    fig.update_xaxes(
        dtick=x_cfg.get("dtick", "M3"),
        tickformat=x_cfg.get("tickformat", "%b %Y"),
        automargin=True, 
        ticks="outside"
    )

    legend_cfg = defaults.get("legend", {})
    fig.update_layout(
        template=site.get("charts", {}).get("template", "simple_white"),
        font=dict(family=site.get("charts", {}).get("font_family", "Inter, sans-serif")),
        height=560,
        margin=dict(l=60, r=24, t=24, b=96),
        legend=dict(
            orientation=legend_cfg.get("orientation", "h"),
            x=0, 
            y=legend_cfg.get("y", 1.05)
        ),
        title=None,
        autosize=True
    )
    
    return fig

def build(chart_type: str, **kwargs):
    """Build a chart using the registry"""
    if chart_type not in _REGISTRY:
        raise ValueError(f"Unknown chart type: {chart_type}. Available types: {list(_REGISTRY.keys())}")
    
    return _REGISTRY[chart_type](**kwargs)
