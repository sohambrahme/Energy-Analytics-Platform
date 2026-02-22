import sqlite3
import pandas as pd
import os

def get_db_connection():
    """Get a connection to the SQLite database."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'energy_warehouse.db')
    return sqlite3.connect(db_path)

def execute_query(query: str, params=None) -> pd.DataFrame:
    """Execute a query and return a pandas DataFrame."""
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_time_series_data(start_date: str = None, end_date: str = None):
    """Retrieve joined energy and weather data for modeling."""
    query = """
    SELECT 
        e.dt_iso as ds,
        e.total_load_actual as y,
        e.price_actual,
        e.total_generation,
        w.avg_temp_c,
        w.avg_humidity,
        w.avg_wind_speed
    FROM fact_energy e
    LEFT JOIN v_national_weather w ON e.dt_iso = w.dt_iso
    WHERE 1=1
    """
    params = []
    if start_date:
        query += " AND e.dt_iso >= ?"
        params.append(f"{start_date} 00:00:00")
    if end_date:
        query += " AND e.dt_iso <= ?"
        params.append(f"{end_date} 23:59:59")
        
    query += " ORDER BY e.dt_iso ASC"
    return execute_query(query, params)
