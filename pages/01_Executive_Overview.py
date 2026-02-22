import streamlit as st
import pandas as pd
from utils.analytics import get_executive_kpis, get_generation_mix, calculate_correlations, get_price_metrics
from utils.transforms import execute_query
from utils.charts import plot_generation_mix, plot_time_series, plot_correlation_heatmap

st.set_page_config(page_title="Executive Overview", page_icon="📈", layout="wide")

st.title("📈 Executive Overview")
st.markdown("High-level Key Performance Indicators for the UK Energy Grid.")

# Load Data
kpis = get_executive_kpis()
price_metrics = get_price_metrics()

if not kpis:
    st.error("No data available. Have you run the data loader?")
    st.stop()

# ----------------------------------------------------
# 1. KPIs
# ----------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Generation", f"{kpis.get('total_generation_mwh', 0) / 1e6:,.2f} TWh")
with col2:
    st.metric("Total Consumption", f"{kpis.get('total_consumption_mwh', 0) / 1e6:,.2f} TWh")
with col3:
    net_twh = kpis.get('net_balance_mwh', 0) / 1e6
    st.metric("Net Balance", f"{net_twh:,.2f} TWh", delta=net_twh)
with col4:
    st.metric("Avg Market Price", f"€{kpis.get('average_price_eur', 0):.2f} / MWh")

st.markdown("---")

# ----------------------------------------------------
# 2. Key Insights & Generation Mix
# ----------------------------------------------------
c1, c2 = st.columns([1, 2])
with c1:
    st.subheader("Business Insights")
    st.markdown(f"""
    - **Market Stability**: Annualized volatility sits at {price_metrics.get('annual_volatility', 0) * 100:.1f}%.
    - **Peak Pricing**: Price ceiling hit €{price_metrics.get('max_price', 0):.2f} with mean of €{price_metrics.get('avg_price', 0):.2f}.
    - **Resource Focus**: Renewable vs Fossil balance is actively captured in the Generation Mix. 
    - **Grid Strategy**: Keep a close eye on the Net Balance. Excessive surplus or deficit periods drive price extremes.
    """)
    st.button("Export KPI Summary", on_click=lambda: st.success("Exported to Local Drive"))

with c2:
    mix_data = get_generation_mix()
    if mix_data:
        # Exclude None or 0
        clean_mix = {k: v for k, v in mix_data.items() if v}
        fig_mix = plot_generation_mix(clean_mix)
        st.plotly_chart(fig_mix, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# 3. Quick Over-Time view
# ----------------------------------------------------
st.subheader("Net Generation Profile")

# Let's get Daily Aggregation of load and gen for faster plotting
query_daily = """
SELECT 
    d.date, 
    SUM(e.total_load_actual) as demand, 
    SUM(e.total_generation) as generation 
FROM fact_energy e
JOIN dim_datetime d ON e.dt_iso = d.dt_iso
GROUP BY d.date
ORDER BY d.date ASC
"""
df_daily = execute_query(query_daily)

if not df_daily.empty:
    fig_time = plot_time_series(
        df_daily, 
        x_col='date', 
        y_cols=['demand', 'generation'],
        title="Daily Demand vs Generation (MWh)"
    )
    st.plotly_chart(fig_time, use_container_width=True)
