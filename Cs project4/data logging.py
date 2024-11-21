import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

data_path = 'atlantic.csv'
hurricane_data = pd.read_csv(data_path)

print("Original Dataset Columns:", hurricane_data.columns)

hurricane_data.rename(columns={
    'Date': 'date',
    'Time': 'time',
    'Event': 'event',
    'Status': 'status',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Maximum Wind': 'wind_speed',
    'Minimum Pressure': 'pressure',
}, inplace=True)

hurricane_data['timestamp'] = pd.to_datetime(hurricane_data['date'].astype(str) + ' ' + hurricane_data['time'].astype(str), errors='coerce')

hurricane_data = hurricane_data.dropna(subset=['timestamp'])

required_columns = ['timestamp', 'event', 'status', 'latitude', 'longitude', 'wind_speed', 'pressure']
assert all(col in hurricane_data.columns for col in required_columns), "Missing required columns!"

logged_data = pd.DataFrame(columns=required_columns)


def update_and_analyze(log, new_entry):
    log = pd.concat([log, pd.DataFrame([new_entry])], ignore_index=True)

    max_wind = log['wind_speed'].max()
    avg_pressure = log['pressure'].mean()
    storm_count = log['event'].value_counts()

    print("\n--- Real-Time Analysis ---")
    print(f"Max Wind Speed: {max_wind} mph")
    print(f"Average Pressure: {avg_pressure:.2f} hPa")
    print(f"Storm Count by Event Type:\n{storm_count}")
    print("--------------------------")

    return log


def plot_real_time(log):
    plt.figure(figsize=(10, 6))
    plt.plot(log['timestamp'], log['wind_speed'], label="Wind Speed (mph)", color='blue', marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Timestamp')
    plt.ylabel('Wind Speed (mph)')
    plt.title('Real-Time Wind Speed Trends')
    plt.grid()
    plt.tight_layout()
    plt.legend()
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()



print("Starting real-time logging of hurricane data...\n")
try:
    for _, row in hurricane_data.iterrows():
        new_data = row.to_dict()
        print(f"New Data Logged: {new_data}")

        logged_data = update_and_analyze(logged_data, new_data)

        plot_real_time(logged_data)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nReal-time logging stopped by user.")

logged_data.to_csv('real_hurricane_data_log.csv', index=False)
print("\nLogged data saved to 'real_hurricane_data_log.csv'.")
