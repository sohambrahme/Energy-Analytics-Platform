import streamlit as st
import pandas as pd
from utils.transforms import get_time_series_data
from utils.forecasting import train_prophet_model, make_forecast, simulate_scenario, calculate_mape
from utils.charts import plot_forecast

st.set_page_config(page_title="Forecast & Scenario Simulator", page_icon="🔮", layout="wide")
st.title("🔮 Load Forecasting & Scenario Simulator")

st.markdown("""
This module uses a **Facebook Prophet** machine learning model to predict energy demand over the next 7 days, based on historical load, seasonality, and exogenous weather factors.
""")

@st.cache_resource(show_spinner="Training Machine Learning Model...")
def load_and_train_model():
    # Only pull the last 365 days for training speed
    # Note: Using hardcoded '2018-01-01' to '2018-12-31' since the dataset is 2015-2018.
    df = get_time_series_data(start_date='2018-01-01', end_date='2018-12-31')
    if df.empty:
        return None, None
    
    # Train test split simply to get the last known date
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
    
    model = train_prophet_model(df, target_col='y', exogenous_cols=['avg_temp_c', 'avg_humidity'])
    return model, df

model, historical_df = load_and_train_model()

if model is None:
    st.error("Could not fetch training data.")
    st.stop()
    
st.success("✅ Prophet Model successfully trained on 2018 dataset.")

st.sidebar.header("Scenario Simulator")
st.sidebar.markdown("Modify exogenous variables to simulate grid load.")

temp_adjustment = st.sidebar.slider("Temperature Offset (°C)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
hum_adjustment = st.sidebar.slider("Humidity Offset (%)", min_value=-50.0, max_value=50.0, value=0.0, step=5.0)

# Make base forecast
# Extract future exogenous baseline
last_30_days = historical_df.tail(168).copy() # Use last week's weather as a simple proxy for the next week
last_30_days['ds'] = last_30_days['ds'] + pd.Timedelta(days=7) # shifting dates into the future
exog_future = last_30_days[['ds', 'avg_temp_c', 'avg_humidity']]

with st.spinner("Generating Forecast Scenario..."):
    # Apply scenario multipliers
    if temp_adjustment != 0 or hum_adjustment != 0:
        modifiers = {}
        if temp_adjustment != 0.0:
            modifiers['avg_temp_c'] = ('add', temp_adjustment)
        if hum_adjustment != 0.0:
            modifiers['avg_humidity'] = ('add', hum_adjustment)
            
        future_forecast = make_forecast(model, periods=168, freq='H', future_exogenous=exog_future)
        scenario_forecast = simulate_scenario(model, future_forecast, modifiers)
        final_forecast = scenario_forecast
        st.info(f"Showing Simulated Scenario (Temp: {temp_adjustment}°C, Humidity: {hum_adjustment}%)")
    else:
        final_forecast = make_forecast(model, periods=168, freq='H', future_exogenous=exog_future)
        st.info("Showing Baseline Forecast")

# Plot combined chart (limit historical to last 14 days to see forecast clearly)
recent_hist = historical_df.tail(14*24)
fig = plot_forecast(recent_hist, final_forecast, "7-Day Load Forecast vs Actuals")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Forecast Data Extract")
st.dataframe(final_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(168), use_container_width=True)
