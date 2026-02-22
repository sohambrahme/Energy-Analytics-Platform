import streamlit as st
import pandas as pd
from utils.transforms import execute_query

st.set_page_config(page_title="Data Quality & Dictionary", page_icon="📋", layout="wide")
st.title("📋 Data Quality & Dictionary")

st.markdown("""
Transparency is crucial in data products. This page outlines data completeness issues, applied treatments, and formal definitions for calculations present in the dashboards.
""")

st.subheader("Data Completeness")

# Quick count of nulls in fact table isn't easily possible in raw since we interpolated.
# But we can show basic row counts.
counts = execute_query("""
SELECT 
    (SELECT COUNT(*) FROM fact_energy) as energy_rows,
    (SELECT COUNT(*) FROM fact_weather) as weather_rows
""")

if not counts.empty:
    c1, c2 = st.columns(2)
    c1.metric("Ingested Energy Timeline (Hours)", counts['energy_rows'].iloc[0])
    c2.metric("Ingested Weather Rows", counts['weather_rows'].iloc[0])

st.markdown("---")

st.subheader("Entity Dictionary")

st.markdown("""
| Column | Type | Business Definition | Treatment |
|---|---|---|---|
| `dt_iso` | Datetime | ISO 8601 Timestamp of the recorded hour. | Converted to UTC. |
| `total_load_actual` | Float | The actual power demand consumed by the grid in MWh. | Linear interpolation for NA values (1%). |
| `price_actual` | Float | The Spot Price resolved on the day in EUR/MWh. | Linear interpolation. |
| `total_generation` | Float | Calculated field summing all active supply generation columns. | SUM(generation_*). Excludes pumped consumption. |
| `net_balance` | Float | Calculated constraint. Total Generation minus Total Load. | `total_generation` - `total_load_actual`. |
| `avg_temp_c` | Float | Weighted average temperature across 5 main UK/ES cites. | Converted from Kelvin (- 273.15). |

### Interpolation Note
During the ETL step (`utils/data_loader.py`), nulls in time series were subjected to linear interpolation to preserve shape for the Facebook Prophet model. Less than 1.5% of the data was synthetic.
""")
