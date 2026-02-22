import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error
from utils.transforms import get_time_series_data

def train_prophet_model(df: pd.DataFrame, target_col: str = 'y', exogenous_cols: list = None):
    """
    Train a Facebook Prophet model.
    df must have 'ds' (datetime) and 'y' (target).
    """
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    
    if exogenous_cols:
        for col in exogenous_cols:
            model.add_regressor(col)
            
    # Prophet requires specific column names
    train_df = df[['ds', target_col]].copy()
    train_df.rename(columns={target_col: 'y'}, inplace=True)
    
    if exogenous_cols:
        for col in exogenous_cols:
            train_df[col] = df[col]
            
    model.fit(train_df)
    return model

def make_forecast(model: Prophet, periods: int = 168, freq: str = 'H', future_exogenous: pd.DataFrame = None):
    """
    Generate future dataframe and predict.
    periods: 168 hours = 7 days
    """
    future = model.make_future_dataframe(periods=periods, freq=freq)
    
    if future_exogenous is not None:
        # Merge future exogenous columns into the future dataframe
        future = future.merge(future_exogenous, on='ds', how='left')
        future.fillna(method='ffill', inplace=True) # basic fill
        future.fillna(method='bfill', inplace=True)
        
    forecast = model.predict(future)
    return forecast

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error."""
    return mean_absolute_percentage_error(y_true, y_pred)

def simulate_scenario(model: Prophet, base_future: pd.DataFrame, scenario_modifiers: dict):
    """
    Run a simulation.
    scenario_modifiers: dict containing percentage or absolute changes for exogenous variables.
    Example: {'temp_c': ('add', 5)} -> increases temp by 5 degrees.
    """
    scenario_future = base_future.copy()
    
    for col, (op, val) in scenario_modifiers.items():
        if col in scenario_future.columns:
            if op == 'add':
                scenario_future[col] += val
            elif op == 'multiply':
                scenario_future[col] *= val
                
    forecast = model.predict(scenario_future)
    return forecast
