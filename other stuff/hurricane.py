import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from scipy.stats import pearsonr

from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import autocorrelation_plot
import statsmodels.api as sm

warnings.filterwarnings('ignore')

data_path = 'atlantic.csv'
data = pd.read_csv(data_path)

print("First few rows of the dataset:")
print(data.head())

data.rename(columns={
    'Maximum Wind': 'wind_speed',
    'Minimum Pressure': 'pressure',
    'Date': 'date',
    'Time': 'time',
    'Latitude': 'latitude',
    'Longitude': 'longitude'
}, inplace=True)

data = data.dropna()

numeric_columns = data.select_dtypes(include=[np.number])

print("\nDataset Summary (Numeric Columns):")
print(numeric_columns.describe())

correlation_matrix = numeric_columns.corr()
print("\nCorrelation Matrix (Numeric Columns):")
print(correlation_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Hurricane Factors (Numeric Data)")
plt.show()

if 'wind_speed' in numeric_columns.columns and 'pressure' in numeric_columns.columns:
    corr_wind_pressure, _ = pearsonr(numeric_columns['wind_speed'], numeric_columns['pressure'])
    print(f"\nCorrelation between Wind Speed and Pressure: {corr_wind_pressure}")

if 'time' in data.columns and 'wind_speed' in numeric_columns.columns:
    plt.figure(figsize=(10, 6))
    plt.plot(data['time'], numeric_columns['wind_speed'], label="Wind Speed", color='blue')
    plt.xlabel('Time')
    plt.ylabel('Wind Speed (mph)')
    plt.title('Wind Speed Over Time')
    plt.grid()
    plt.legend()
    plt.show()

if 'time' in data.columns and 'pressure' in numeric_columns.columns and 'latitude' in numeric_columns.columns:
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Pressure (hPa)', color='red')
    ax1.plot(data['time'], numeric_columns['pressure'], color='red', label="Pressure")
    ax1.tick_params(axis='y', labelcolor='red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Latitude', color='blue')
    ax2.plot(data['time'], numeric_columns['latitude'], color='blue', label="Latitude")
    ax2.tick_params(axis='y', labelcolor='blue')

    fig.tight_layout()
    plt.title("Pressure and Latitude Over Time")
    plt.show()

if 'wind_speed' in data.columns:
    try:
        wind_speed_series = pd.to_numeric(data['wind_speed'], errors='coerce').dropna()
        model = ARIMA(wind_speed_series, order=(5, 1, 0))
        model_fit = model.fit()
        print("\nARIMA Model Summary:")
        print(model_fit.summary())

        plt.figure(figsize=(10, 6))
        plt.plot(wind_speed_series.reset_index(drop=True), label="Original")
        plt.plot(model_fit.fittedvalues, label="Fitted Values", color='red')
        plt.title("ARIMA Model - Fitted Values vs Original")
        plt.legend()
        plt.show()
    except ValueError as e:
        print(f"ARIMA modeling error: {e}")