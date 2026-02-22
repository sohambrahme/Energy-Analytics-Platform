import pandas as pd
import numpy as np
import scipy.stats as stats
from utils.transforms import execute_query

def get_executive_kpis():
    """Fetch high-level KPIs."""
    query = "SELECT * FROM v_executive_kpis LIMIT 1"
    df = execute_query(query)
    if not df.empty:
        return df.iloc[0].to_dict()
    return {}

def get_generation_mix():
    """Fetch total generation by source."""
    query = "SELECT * FROM v_generation_mix LIMIT 1"
    df = execute_query(query)
    if not df.empty:
        return df.iloc[0].to_dict()
    return {}

def get_daily_peaks():
    """Fetch daily peak demands."""
    query = "SELECT * FROM v_daily_peak_demand ORDER BY date ASC"
    return execute_query(query)

def calculate_correlations(df: pd.DataFrame, target_col: str, feature_cols: list) -> pd.DataFrame:
    """Calculate Pearson and Spearman correlations against a target."""
    results = []
    
    # Drop NAs
    df_clean = df[[target_col] + feature_cols].dropna()
    
    for col in feature_cols:
        pearson_corr, _ = stats.pearsonr(df_clean[target_col], df_clean[col])
        spearson_corr, _ = stats.spearmanr(df_clean[target_col], df_clean[col])
        
        results.append({
            'Feature': col,
            'Pearson': round(pearson_corr, 3),
            'Spearman': round(spearson_corr, 3)
        })
        
    res_df = pd.DataFrame(results).sort_values('Pearson', ascending=False)
    return res_df

def get_price_metrics():
    """Calculate price volatility and basic distribution stats."""
    query = "SELECT dt_iso, price_actual FROM fact_energy"
    df = execute_query(query)
    if df.empty:
        return {}
    
    df['dt_iso'] = pd.to_datetime(df['dt_iso'])
    df.set_index('dt_iso', inplace=True)
    
    daily_price = df.resample('D').mean()
    volatility = daily_price['price_actual'].pct_change().std() * np.sqrt(365) # Annualized
    
    return {
        'avg_price': df['price_actual'].mean(),
        'max_price': df['price_actual'].max(),
        'min_price': df['price_actual'].min(),
        'annual_volatility': volatility
    }
