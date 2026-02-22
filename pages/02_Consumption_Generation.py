import streamlit as st
import pandas as pd
from utils.transforms import execute_query
from utils.charts import plot_time_series, plot_stacked_area

st.set_page_config(page_title="Consumption & Generation", page_icon="🏭", layout="wide")
st.title("🏭 Consumption & Generation Analytics")

# Basic time filter
st.sidebar.header("Filters")
min_max_dates = execute_query("SELECT MIN(date) as min_dt, MAX(date) as max_dt FROM dim_datetime").iloc[0]
start_dt, end_dt = st.sidebar.date_input("Date Range", [pd.to_datetime(min_max_dates['min_dt']).date(), pd.to_datetime(min_max_dates['max_dt']).date()])

# Time-series trend
st.subheader("Time Series: Load vs Total Generation")
query_ts = f"""
    SELECT 
        d.date,
        SUM(e.total_load_actual) as demand,
        SUM(e.total_generation) as generation
    FROM fact_energy e
    JOIN dim_datetime d ON e.dt_iso = d.dt_iso
    WHERE d.date BETWEEN '{start_dt}' AND '{end_dt}'
    GROUP BY d.date
    ORDER BY d.date ASC
"""
df_ts = execute_query(query_ts)

if not df_ts.empty:
    fig_ts = plot_time_series(df_ts, 'date', ['demand', 'generation'], "Daily Demand vs Generation (MWh)")
    st.plotly_chart(fig_ts, use_container_width=True)

# Stacked Area Fuel Mix
st.subheader("Fuel Mix Over Time")
query_mix = f"""
    SELECT 
        d.date,
        SUM(e.generation_biomass) as biomass,
        SUM(e.generation_fossil_brown_coal) as brown_coal,
        SUM(e.generation_fossil_gas) as gas,
        SUM(e.generation_fossil_hard_coal) as hard_coal,
        SUM(e.generation_nuclear) as nuclear,
        SUM(e.generation_solar) as solar,
        SUM(e.generation_wind_onshore) as wind,
        SUM(e.generation_hydro_run_of_river) + SUM(e.generation_hydro_water_reservoir) as hydro
    FROM fact_energy e
    JOIN dim_datetime d ON e.dt_iso = d.dt_iso
    WHERE d.date BETWEEN '{start_dt}' AND '{end_dt}'
    GROUP BY d.date
    ORDER BY d.date ASC
"""
df_fuel = execute_query(query_mix)

if not df_fuel.empty:
    fig_area = plot_stacked_area(df_fuel, 'date', "Energy Mix Contribution (Daily MWh)")
    st.plotly_chart(fig_area, use_container_width=True)

st.markdown("""
### Analyst Notes:
- **Renewable Intermittency**: Notice the variance in Onshore Wind and Solar generation.
- **Base Load**: Nuclear and Gas remain the primary base load maintainers.
- **Export Data**:
""")

csv = df_ts.to_csv(index=False).encode('utf-8')
st.download_button(
    "📥 Download Load Data as CSV",
    csv,
    "load_generation.csv",
    "text/csv",
)
