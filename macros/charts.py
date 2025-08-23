# Chart registry and theme system
from dataclasses import dataclass
from typing import Callable, Dict, List
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
    colorway: List[str]
    template: str
    font: str
    title_size: int
    axis_size: int
    grid: bool

def load_theme() -> Theme:
    """Load theme configuration from site.yml"""
    site_path = Path("docs/_data/site.yml")
    if not site_path.exists():
        # Fallback theme if site.yml doesn't exist
        return Theme(
            colorway=["#005EB8", "#00A3E0", "#FFC300"],
            template="simple_white",
            font="Inter, sans-serif",
            title_size=20,
            axis_size=12,
            grid=True
        )
    
    site = yaml.safe_load(site_path.read_text())
    c = site["charts"]["colors"]
    charts_config = site["charts"]
    
    return Theme(
        colorway=[c["primary"], c["secondary"], c["accent"], c.get("neutral", "#5F6A6A"), c.get("gray", "#D5D8DC")],
        template=charts_config.get("template", "simple_white"),
        font=charts_config["font_family"],
        title_size=charts_config["title_size"],
        axis_size=charts_config.get("axis_size", 12),
        grid=charts_config.get("grid", True)
    )

@chart("line_multi")
def line_multi(data: str, params: dict):
    """Multi-line chart builder"""
    th = load_theme()
    df = pd.read_csv(data)
    
    fig = px.line(
        df, 
        x=params["x"], 
        y=params["ys"], 
        title=params.get("title", "")
    )
    
    # Apply theme
    fig.update_layout(
        template=th.template,
        colorway=th.colorway,
        font=dict(family=th.font),
        title_font_size=th.title_size,
        xaxis=dict(tickfont=dict(size=th.axis_size)),
        yaxis=dict(tickfont=dict(size=th.axis_size)),
        showlegend=True
    )
    
    # Style traces
    fig.update_traces(line=dict(width=2))
    
    # Grid settings
    if th.grid:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

@chart("bar_grouped")
def bar_grouped(data: str, params: dict):
    """Grouped bar chart builder"""
    th = load_theme()
    df = pd.read_csv(data)
    
    fig = px.bar(
        df,
        x=params["x"],
        y=params["y"],
        color=params.get("color"),
        title=params.get("title", ""),
        barmode='group'
    )
    
    # Apply theme
    fig.update_layout(
        template=th.template,
        colorway=th.colorway,
        font=dict(family=th.font),
        title_font_size=th.title_size,
        xaxis=dict(tickfont=dict(size=th.axis_size)),
        yaxis=dict(tickfont=dict(size=th.axis_size))
    )
    
    if th.grid:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

@chart("scatter_trend")
def scatter_trend(data: str, params: dict):
    """Scatter plot with trend line"""
    th = load_theme()
    df = pd.read_csv(data)
    
    fig = px.scatter(
        df,
        x=params["x"],
        y=params["y"],
        color=params.get("color"),
        title=params.get("title", ""),
        trendline="ols" if params.get("trendline", True) else None
    )
    
    # Apply theme
    fig.update_layout(
        template=th.template,
        colorway=th.colorway,
        font=dict(family=th.font),
        title_font_size=th.title_size,
        xaxis=dict(tickfont=dict(size=th.axis_size)),
        yaxis=dict(tickfont=dict(size=th.axis_size))
    )
    
    if th.grid:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig

def build(chart_type: str, data: str, params: dict):
    """Build a chart using the registry"""
    if chart_type not in _REGISTRY:
        raise ValueError(f"Unknown chart type: {chart_type}. Available types: {list(_REGISTRY.keys())}")
    
    return _REGISTRY[chart_type](data, params)

def list_chart_types() -> List[str]:
    """List all available chart types"""
    return list(_REGISTRY.keys())
