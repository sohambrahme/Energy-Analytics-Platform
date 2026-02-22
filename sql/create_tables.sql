-- File: sql/create_tables.sql

-- Drop tables if they exist to allow clean reload
DROP TABLE IF EXISTS fact_weather;
DROP TABLE IF EXISTS fact_energy;
DROP TABLE IF EXISTS dim_datetime;

-- Create Dimension Table for Date and Time
CREATE TABLE dim_datetime (
    dt_iso TEXT PRIMARY KEY,
    date TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    day_of_week INTEGER,
    is_weekend INTEGER
);

-- Create Fact Table for Energy Generation, Consumption, and Prices
CREATE TABLE fact_energy (
    dt_iso TEXT PRIMARY KEY,
    generation_biomass REAL,
    generation_fossil_brown_coal REAL,
    generation_fossil_gas REAL,
    generation_fossil_hard_coal REAL,
    generation_fossil_oil REAL,
    generation_hydro_pumped_consumption REAL,
    generation_hydro_run_of_river REAL,
    generation_hydro_water_reservoir REAL,
    generation_nuclear REAL,
    generation_other REAL,
    generation_other_renewable REAL,
    generation_solar REAL,
    generation_waste REAL,
    generation_wind_onshore REAL,
    total_load_actual REAL,
    price_actual REAL,
    total_generation REAL,
    net_balance REAL,
    FOREIGN KEY(dt_iso) REFERENCES dim_datetime(dt_iso)
);

-- Create Fact Table for Weather Data (grouped by city)
CREATE TABLE fact_weather (
    dt_iso TEXT,
    city_name TEXT,
    temp REAL,
    pressure REAL,
    humidity REAL,
    wind_speed REAL,
    rain_1h REAL,
    snow_3h REAL,
    clouds_all INTEGER,
    weather_main TEXT,
    PRIMARY KEY (dt_iso, city_name),
    FOREIGN KEY(dt_iso) REFERENCES dim_datetime(dt_iso)
);
