import streamlit as st
import pandas as pd
from utils.transforms import execute_query
from utils.analytics import calculate_correlations
from utils.charts import plot_correlation_heatmap

st.set_page_config(page_title="Weather Impact", page_icon="🌦️", layout="wide")
st.title("🌦️ Weather Impact & Correlation Modelling")

st.markdown("Understanding how meteorological conditions affect base load and renewable output performance.")

# Data Pull
query_weather_model = """
SELECT 
    e.total_load_actual,
    e.price_actual,
    w.avg_temp_c,
    w.avg_humidity,
    w.avg_wind_speed,
    w.avg_clouds
FROM fact_energy e
JOIN v_national_weather w ON e.dt_iso = w.dt_iso
"""
df_model = execute_query(query_weather_model)

if not df_model.empty:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Load Correlation Matrix")
        # Compute correlations against Load
        corr_df = calculate_correlations(
            df_model, 
            target_col='total_load_actual', 
            feature_cols=['avg_temp_c', 'avg_humidity', 'avg_wind_speed', 'avg_clouds']
        )
        st.dataframe(corr_df.style.background_gradient(cmap='Blues'), use_container_width=True)
        
        st.markdown("""
        **Observations:**
        - **Temperature**: Often explicitly inversely correlated to load in cold climates (heating load).
        - **Humidity/Clouds**: Affects PV solar generation, translating to higher demands on grid base loads.
        """)

    with col2:
        st.subheader("Global Correlation Heatmap")
        # Global Heatmap
        features = ['total_load_actual', 'price_actual', 'avg_temp_c', 'avg_humidity', 'avg_wind_speed']
        fig_heat = plot_correlation_heatmap(df_model, features, "Demand & Weather Auto-Correlation")
        st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.warning("For advanced causal modeling, residuals from an ARIMA model should be extracted to isolate non-weather elements.")
