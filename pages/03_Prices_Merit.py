import streamlit as st
import pandas as pd
import plotly.express as px
from utils.transforms import execute_query
from utils.charts import plot_scatter_with_trend, apply_layout

st.set_page_config(page_title="Prices & Merit Order", page_icon="💶", layout="wide")
st.title("💶 Market Prices & Demand Merit")

# Fetch data for distribution
st.subheader("Wholesale Price Distribution")
query_prices = "SELECT price_actual FROM fact_energy WHERE price_actual IS NOT NULL"
df_prices = execute_query(query_prices)

if not df_prices.empty:
    fig_hist = px.histogram(df_prices, x="price_actual", nbins=100, title="Price Density (EUR/MWh)", opacity=0.8, color_discrete_sequence=["#2ca02c"])
    fig_hist = apply_layout(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

st.subheader("Price Sensitivity to Demand")
st.markdown("Higher load generally dictates that more expensive (fossil) assets hit the merit order, driving marginal prices upwards.")

# Scatter Plot
query_scatter = """
    SELECT 
        e.total_load_actual as demand,
        e.price_actual as price,
        d.is_weekend
    FROM fact_energy e
    JOIN dim_datetime d ON e.dt_iso = d.dt_iso
    WHERE e.total_load_actual IS NOT NULL AND e.price_actual IS NOT NULL
"""
df_scatter = execute_query(query_scatter)

if not df_scatter.empty:
    # Adding a class for Weekend coloring
    df_scatter['Day Type'] = df_scatter['is_weekend'].apply(lambda x: "Weekend" if x == 1 else "Weekday")
    
    # We sample it because drawing 35,000 scatter points is heavy on the browser
    sample_df = df_scatter.sample(n=min(5000, len(df_scatter)), random_state=42)
    
    fig_scatter = plot_scatter_with_trend(
        sample_df, 
        x_col="demand", 
        y_col="price", 
        title="Demand vs Spot Price (Random 5k Sample)"
    )
    # Re-apply color map for day type
    fig_scatter = px.scatter(
        sample_df, x="demand", y="price", 
        color="Day Type", opacity=0.6,
        title="Price Sensitivity (Sampled)"
    )
    fig_scatter = apply_layout(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

st.info("💡 **Insight**: The merit order effect is visible. During weekends, demand drops and prices remain at the lowest quartile.")
