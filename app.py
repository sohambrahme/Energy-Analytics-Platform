import streamlit as st
import os

st.set_page_config(
    page_title="UK Energy Analytics Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the main app
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 16px;
    }
    .metric-title {
        color: #6c757d;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #212529;
        font-size: 24px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ UK Energy Analytics Platform")

st.markdown("""
Welcome to the internal **Energy Analytics Platform**. This workspace is designed for grid operators, energy traders, and stakeholders to monitor network balance, generation mix, weather impact, and forecast energy demand.

### 🌟 Platform Capabilities
- **Executive Overview**: High-level KPIs including net balance and average market price.
- **Consumption & Generation Analysis**: Detailed historical trends of load and mixed generation sources.
- **Prices & Merit Order**: Market pricing analysis, price volatility, and supply/demand merit.
- **Weather Impact**: Correlation models showing how weather drives power consumption.
- **Forecast & Scenario Simulator**: Machine learning models pointing to expected peak loads and impact of different scenarios.
- **Data Governance**: Detailed logging of data completeness and missing values.

👈 **Please select a page from the sidebar to begin analyzing the grid data.**
""")

st.info("💡 **Tip**: Use the sidebar globally to filter data across all analytic views.")

# Check DB exists
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'data', 'energy_warehouse.db')

if not os.path.exists(db_path):
    st.warning("⚠️ Data Warehouse not found. Please run `python utils/data_loader.py` to initialize local data.")
else:
    st.success("✅ Connected to SQLite Data Warehouse.")
