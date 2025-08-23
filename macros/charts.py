# Chart registry and theme system
from dataclasses import dataclass
from typing import Callable, Dict
from pathlib import Path
import yaml
import pandas as pd
import plotly.express as px

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

def apply_theme_and_responsive(fig, theme: Theme):
    """Apply theme and responsive settings to a figure"""
    fig.update_layout(
        template=theme.template,
        colorway=theme.colors,
        font=dict(family=theme.font),
        title_font_size=theme.title_size,
        # Responsive margins and sizing
        margin=dict(l=40, r=10, t=40, b=40),
        autosize=True
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
    
    # Style traces
    fig.update_traces(line=dict(width=2))
    
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

def build(chart_type: str, **kwargs):
    """Build a chart using the registry"""
    if chart_type not in _REGISTRY:
        raise ValueError(f"Unknown chart type: {chart_type}. Available types: {list(_REGISTRY.keys())}")
    
    return _REGISTRY[chart_type](**kwargs)
