import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict

# Theme settings
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
BACKGROUND_COLOR = "#f8f9fa"

def apply_layout(fig):
    """Apply consistent styling to all charts."""
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=40, l=40, b=40, r=40),
        font=dict(family="Inter, Roboto, sans-serif", size=12),
        title_font=dict(size=16, family="Inter, Roboto, sans-serif"),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e9ecef')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e9ecef')
    return fig

def plot_time_series(df: pd.DataFrame, x_col: str, y_cols: list, title: str):
    """Plot simple line charts."""
    fig = px.line(df, x=x_col, y=y_cols, title=title)
    fig = apply_layout(fig)
    return fig

def plot_generation_mix(mix_dict: Dict[str, float]):
    """Plot generation mix as a Donut or Bar chart."""
    df = pd.DataFrame(list(mix_dict.items()), columns=['Source', 'MWh'])
    df = df[df['MWh'] > 0].sort_values('MWh', ascending=True)
    
    fig = px.bar(df, x='MWh', y='Source', orientation='h', title="Generation Mix (MWh)", color='Source')
    fig.update_layout(showlegend=False)
    fig = apply_layout(fig)
    return fig

def plot_stacked_area(df: pd.DataFrame, x_col: str, title: str = "Energy Mix Over Time"):
    """Plot stacked area for energy contribution."""
    cols_to_plot = [c for c in df.columns if c != x_col]
    fig = px.area(df, x=x_col, y=cols_to_plot, title=title)
    fig = apply_layout(fig)
    return fig

def plot_correlation_heatmap(df: pd.DataFrame, cols: list, title: str = "Correlation Heatmap"):
    """Plot correlation heatmap."""
    corr = df[cols].corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title=title
    )
    fig.update_layout(margin=dict(t=40, l=40, b=40, r=40))
    return fig

def plot_scatter_with_trend(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    """Plot scatter plot mapping demand vs price."""
    fig = px.scatter(
        df, x=x_col, y=y_col, 
        trendline="ols", 
        opacity=0.5,
        title=title,
        color_discrete_sequence=[PRIMARY_COLOR]
    )
    fig = apply_layout(fig)
    return fig

def plot_forecast(df_hist: pd.DataFrame, df_forecast: pd.DataFrame, title: str):
    """Plot historical and forecasted data side by side."""
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=df_hist['ds'], y=df_hist['y'],
        mode='lines', name='Actual',
        line=dict(color=PRIMARY_COLOR)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=df_forecast['ds'], y=df_forecast['yhat'],
        mode='lines', name='Forecast',
        line=dict(color=SECONDARY_COLOR)
    ))
    
    # Uncertainty
    fig.add_trace(go.Scatter(
        x=df_forecast['ds'], y=df_forecast['yhat_upper'],
        mode='lines', line=dict(width=0),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=df_forecast['ds'], y=df_forecast['yhat_lower'],
        mode='lines', line=dict(width=0),
        fill='tonexty', fillcolor='rgba(255, 127, 14, 0.2)',
        name='Uncertainty Interval'
    ))
    
    fig.update_layout(title=title)
    fig = apply_layout(fig)
    return fig
