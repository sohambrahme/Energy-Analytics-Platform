-- File: sql/kpi_queries.sql

-- 1. Total KPI View
CREATE VIEW IF NOT EXISTS v_executive_kpis AS
SELECT 
    SUM(total_generation) as total_generation_mwh,
    SUM(total_load_actual) as total_consumption_mwh,
    SUM(net_balance) as net_balance_mwh,
    AVG(price_actual) as average_price_eur
FROM fact_energy;

-- 2. Generation Mix Summary
CREATE VIEW IF NOT EXISTS v_generation_mix AS
SELECT 
    SUM(generation_biomass) as biomass,
    SUM(generation_fossil_brown_coal) as brown_coal,
    SUM(generation_fossil_gas) as gas,
    SUM(generation_fossil_hard_coal) as hard_coal,
    SUM(generation_fossil_oil) as oil,
    SUM(generation_hydro_run_of_river) + SUM(generation_hydro_water_reservoir) as hydro,
    SUM(generation_nuclear) as nuclear,
    SUM(generation_solar) as solar,
    SUM(generation_wind_onshore) as wind,
    SUM(generation_waste) as waste,
    SUM(generation_other) + SUM(generation_other_renewable) as other
FROM fact_energy;

-- 3. Daily Peak Demand
CREATE VIEW IF NOT EXISTS v_daily_peak_demand AS
SELECT
    d.date,
    MAX(e.total_load_actual) as peak_demand,
    AVG(e.price_actual) as daily_avg_price
FROM fact_energy e
JOIN dim_datetime d ON e.dt_iso = d.dt_iso
GROUP BY d.date;

-- 4. National Weather Averages (Averaged across regions per hour)
CREATE VIEW IF NOT EXISTS v_national_weather AS
SELECT
    dt_iso,
    AVG(temp) - 273.15 as avg_temp_c, -- converting from Kelvin
    AVG(humidity) as avg_humidity,
    AVG(wind_speed) as avg_wind_speed,
    AVG(clouds_all) as avg_clouds
FROM fact_weather
GROUP BY dt_iso;
