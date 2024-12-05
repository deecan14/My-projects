import pandas as pd # Modules to be imported
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# Using OS module to find and specify data path of atlantic.csv
directory = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(directory, 'atlantic.csv')
hurricane_data = pd.read_csv(data_path)

print("Original Dataset Columns:", hurricane_data.columns) # Printing original columns

hurricane_data.rename(columns={ # Renaming columns for easier access and removing spaces/capitalization
    'Date': 'date',
    'Time': 'time',
    'Event': 'event',
    'Status': 'status',
    'Latitude': 'latitude',
    'Longitude': 'longitude',
    'Maximum Wind': 'wind_speed',
    'Minimum Pressure': 'pressure',
}, inplace=True)

# Converting date and time into 'timestamp' column creates a warning in the console. 
#   - This is normal and expected, and it does not affect code functionality.
hurricane_data['timestamp'] = pd.to_datetime(hurricane_data['date'].astype(str) + ' ' + hurricane_data['time'].astype(str), errors='coerce')

hurricane_data = hurricane_data.dropna(subset=['timestamp']) # Failsafe to remove invalid timestamps 

# Verifies that required columns are in pandas database
required_columns = ['timestamp', 'event', 'status', 'latitude', 'longitude', 'wind_speed', 'pressure']
assert all(col in hurricane_data.columns for col in required_columns), "Missing required columns!"

# Sort hurricane_data by timestamp
hurricane_data = hurricane_data.sort_values(by='timestamp', ascending=True)

logged_data = pd.DataFrame(columns=required_columns) # Creates a dataframe


def update_and_analyze(log, new_entry): # Function to convert data from dataframe into information for user in console
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


def plot_real_time(log, Legacy=False, Close=True): # Plotting function, has option for legacy mode or normal (default).
    if Legacy: # Legacy is available when the default mode is too processor intensive. Reccomended not to use for most cases.
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
        plt.pause(0.5)
        if Close:
            plt.close()
    else: # Default method of plotting (reccomended)
        plt.clf()
        plt.plot(log['timestamp'], log['wind_speed'], label="Wind Speed (mph)", color='blue', marker='o')
        plt.draw()
        plt.pause(0.01)


# Before plotting and processing data, optionally ask user to choose custom date range!
print("Type a range of years to process hurricane data between 1851 and 2023. Default: 1851-2023")
yrrange = input()
if yrrange == None: # If no range is typed, use default (1851 - 2023)
    yrrange = "1851-2023"
while True: # Verifies that date range was typed in correct format, creates startYr and endYr vars
    try:
        yrrange = yrrange.split('-')
        startYr = int(yrrange[0])
        endYr = int(yrrange[1])
        if endYr > startYr:
            break
        else:
            raise ValueError() # Raises error, causing except clause to run and loop to continue.
    except: # Occurs when range is typed incorrectly.
        print("Error: incorrect syntax. Use the format 'XXXX-YYYY', replacing XXXX and YYYY with years between 1851 and 2023.")
        print("\nVerify that XXXX is less than YYYY. Example: 2010-2015")
        yrrange = input()

# Adding new column in pandas (yr) from timestamp's first 4 characters
hurricane_data['yr'] = hurricane_data['timestamp'].astype(str).str[:4]

# Converting startYr and endYr to indexes to process data only in specific time frame
startYrIndx = hurricane_data[hurricane_data['yr'] == str(startYr)].index[0]
endYrIndx = hurricane_data[hurricane_data['yr'] == str(endYr)].index[-1]

# Filtering hurricane_data to only include specific years requested by user
hurricane_data = hurricane_data.loc[startYrIndx:endYrIndx]

print("Use legacy mode? (Legacy plots data slower, by rapidly opening and closing the graph, but may be easier on processing power and less prone to error.)")
print("Default is false.\nType '2' to use legacy mode or press Enter to use default mode.")
userInput = input() # Asks to use legacy mode, saves choice as variable
if userInput == "2":
    legacyMode = True
else:
    legacyMode = False

print("Starting real-time logging of hurricane data...\n") # Processing begins
try:
    if legacyMode: # If legacy mode was chosen by user
        for _, row in hurricane_data.iterrows():
            new_data = row.to_dict()
            print(f"New Data Logged: {new_data}")

            logged_data = update_and_analyze(logged_data, new_data)

            plot_real_time(logged_data, Legacy=True)

            time.sleep(0.5)
    else: # Default processing!
        plt.ion()
        plt.xlabel('Timestamp')
        plt.ylabel('Wind Speed (mph)')
        plt.title('Real-Time Wind Speed Trends')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.legend()
        for _, row in hurricane_data.iterrows():
            new_data = row.to_dict()
            print(f"New Data Logged: {new_data}")

            logged_data = update_and_analyze(logged_data, new_data)

            plot_real_time(logged_data)
        
        plt.xlabel('Timestamp')
        plt.ylabel('Wind Speed (mph)')
        plt.title('Real-Time Wind Speed Trends')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.legend()

except KeyboardInterrupt: # Allows user to stop processing using CTRL+C
    # Plotting can take some time
    print("\nReal-time logging stopped by user.")

while True: # Loops to prevent a user from crashing program because they held CTRL+C
    try:
        time.sleep(1)
        logged_data.to_csv('real_hurricane_data_log.csv', index=False)
        print("\nLogged data saved to 'real_hurricane_data_log.csv'.") # Saves data into csv
        time.sleep(1)
        if legacyMode:
            plot_real_time(logged_data, Legacy=True, Close=False)
        print("\nPress Enter to exit and close graph...")
        input()
        break # End of program
    except KeyboardInterrupt:
        print("Please let go of Ctrl + C!")

        