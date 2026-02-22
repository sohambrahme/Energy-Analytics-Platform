# UK Energy Analytics Platform

A professional end-to-end Energy Analytics Platform built as a multi-page Streamlit application. This project showcases data engineering, SQL analytics, time-series forecasting, and interactive stakeholder reporting tailored for UK energy and utilities data analyst roles.

## Business Problem
Energy markets are highly complex, with dynamics driven by consumption behavior, renewable generation intermittency, merit order pricing, and weather impacts. Analysts need robust tools to combine disparate datasets (generation mix, pricing, weather factors) to understand historical trends, identify correlations, and simulate future scenarios. This platform solves the problem by providing an interactive, centralized dashboard for these core requirements.

## Dataset
This project uses the "Energy Consumption, Generation, Prices, and Weather" dataset from Kaggle:
https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather

The dataset contains energy consumption, generation per type, pricing, and weather data. Please download the dataset and place the CSV files inside the `data/` directory before running the pipeline.

## KPI Definitions
- **Total Consumption**: Total energy consumed across the selected period.
- **Total Generation**: Total energy generated across the selected period.
- **Net Balance**: The difference between Total Generation and Total Consumption.
- **Average Market Price**: Mean price of energy in the wholesale market.
- **Peak Demand**: Highest hourly consumption demand recorded.

## Skills Demonstrated
- **SQL Data Warehouse**: Building a star schema with dimension and fact tables in SQLite.
- **Data Engineering**: Data cleaning, harmonization, and pipeline orchestrations with Python & Pandas.
- **Business Intelligence**: Developing multi-page, interactive BI dashboards with Streamlit and Plotly.
- **Advanced Analytics**: Correlative analysis, regression modeling for price vs. demand.
- **Time-Series Forecasting**: Utilizing Facebook Prophet for demand and price forecasting.
- **Scenario Simulation**: Interactive modeling of inputs (e.g., weather events) on future energy demand.

## Setup & Running Locally

1. **Environment Setup**:
   Ensure you have Python 3.9+ installed. Create a virtual environment and install the requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Data Pipeline**:
   Download the datasets into the `data/` directory. Initialize the SQLite data warehouse:
   ```bash
   python utils/data_loader.py
   ```

3. **Run the Application**:
   Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Cloud
1. Push this repository to GitHub.
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/).
3. Create a new app, select your repository, branch, and `app.py` as the main file.
4. Add any necessary secrets if applicable (none required for this SQLite deployment).
5. Click **Deploy**.
