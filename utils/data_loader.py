import pandas as pd
import numpy as np
import sqlite3
import os
import pytz

def clean_energy_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the energy dataset."""
    print("Cleaning energy data...")
    # Convert time to UTC datetime, then format as ISO 8601 string
    df['dt_iso'] = pd.to_datetime(df['time'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
    df.drop(columns=['time'], inplace=True)
    
    # Drop columns with mostly missing or 0 values
    drop_cols = [
        'generation fossil coal-derived gas',
        'generation fossil oil shale',
        'generation fossil peat',
        'generation geothermal',
        'generation hydro pumped storage aggregated',
        'generation marine',
        'generation wind offshore',
        'forecast solar day ahead',
        'forecast wind offshore eday ahead',
        'forecast wind onshore day ahead',
        'total load forecast',
        'price day ahead'
    ]
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)
    
    # Clean column names
    df.columns = df.columns.str.replace(r'[^a-zA-Z0-9]+', '_', regex=True).str.lower()
    df.rename(columns={
        'generation_hydro_pumped_storage_consumption': 'generation_hydro_pumped_consumption',
        'generation_fossil_brown_coal_lignite': 'generation_fossil_brown_coal',
        'generation_hydro_run_of_river_and_poundage': 'generation_hydro_run_of_river'
    }, inplace=True)
    
    # Fill NAs with interpolation
    df.interpolate(method='linear', limit_direction='both', inplace=True)
    
    # Calculate Total Generation and Net Balance
    generation_cols = [c for c in df.columns if c.startswith('generation_') and 'consumption' not in c]
    df['total_generation'] = df[generation_cols].sum(axis=1)
    df['net_balance'] = df['total_generation'] - df['total_load_actual']
    
    # Deduplicate dt_iso
    df.drop_duplicates(subset=['dt_iso'], keep='first', inplace=True)
    return df

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the weather dataset."""
    print("Cleaning weather data...")
    # Parse dates
    df['dt_iso'] = pd.to_datetime(df['dt_iso'], utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Drop duplicates
    df.drop_duplicates(subset=['dt_iso', 'city_name'], keep='first', inplace=True)
    
    # Keep essential columns
    keep_cols = ['dt_iso', 'city_name', 'temp', 'pressure', 'humidity', 'wind_speed', 'rain_1h', 'snow_3h', 'clouds_all', 'weather_main']
    df = df[[c for c in keep_cols if c in df.columns]]
    
    # Fill NAs
    df.fillna(0, inplace=True)
    return df

def generate_dim_datetime(dt_series: pd.Series) -> pd.DataFrame:
    """Generate datetime dimension table."""
    print("Generating dimension dates...")
    dts = pd.to_datetime(dt_series)
    df = pd.DataFrame({'dt_iso': dt_series})
    df['date'] = dts.dt.date.astype(str)
    df['year'] = dts.dt.year
    df['month'] = dts.dt.month
    df['day'] = dts.dt.day
    df['hour'] = dts.dt.hour
    df['day_of_week'] = dts.dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    return df

def load_data_to_sqlite(db_path: str, energy_csv: str, weather_csv: str, sql_ddl: str, sql_views: str):
    """Orchestrate ETL to SQLite."""
    print("Starting data ingestion process...")
    
    energy_df = pd.read_csv(energy_csv)
    energy_df = clean_energy_data(energy_df)
    
    weather_df = pd.read_csv(weather_csv)
    weather_df = clean_weather_data(weather_df)
    
    dim_dt = generate_dim_datetime(energy_df['dt_iso'])
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Executing DDL...")
    with open(sql_ddl, 'r') as f:
        cursor.executescript(f.read())
        
    print("Inserting data into DB...")
    dim_dt.to_sql('dim_datetime', conn, if_exists='append', index=False)
    energy_df.to_sql('fact_energy', conn, if_exists='append', index=False)
    weather_df.to_sql('fact_weather', conn, if_exists='append', index=False)
    
    print("Creating views...")
    with open(sql_views, 'r') as f:
        cursor.executescript(f.read())
        
    conn.commit()
    conn.close()
    print(f"Data ingestion complete. Database saved to {db_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, 'data', 'energy_warehouse.db')
    energy_csv = os.path.join(BASE_DIR, 'data', 'energy_dataset.csv')
    weather_csv = os.path.join(BASE_DIR, 'data', 'weather_features.csv')
    sql_ddl = os.path.join(BASE_DIR, 'sql', 'create_tables.sql')
    sql_views = os.path.join(BASE_DIR, 'sql', 'kpi_queries.sql')
    
    if os.path.exists(db_path):
        print("Database already exists. Removing to rebuild...")
        os.remove(db_path)
        
    load_data_to_sqlite(db_path, energy_csv, weather_csv, sql_ddl, sql_views)
