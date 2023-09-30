import pandas as pd

# Read the Excel file into a DataFrame, specifying the 'Time' column as datetime
df = pd.read_excel("hibah.xlsx", parse_dates=['Time'])

# Extract relevant columns
df = df[['Time', 'User MAC Address', 'User ID', 'AP Name', 'AP MAC Address']]

# Sort the DataFrame by 'Time'
df = df.sort_values(by='Time')

# Create a new column 'Next_Time' to represent the next row's 'Time' value
df['Next_Time'] = df['Time'].shift(-1)

# Format the 'Time' and 'Next_Time' columns as strings in a format that Excel can easily read
df['Time'] = df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['Next_Time'] = df['Next_Time'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Initialize variables to track connected intervals
current_user_mac = None
current_user_id = None
current_ap_name = None
current_start_time = None
connected_intervals = []

# Iterate through rows to identify connected intervals
for index, row in df.iterrows():
    if current_user_mac is None:
        current_user_mac = row['User MAC Address']
        current_user_id = row['User ID']
        current_ap_name = row['AP Name']
        current_start_time = row['Time']
    elif row['User MAC Address'] == current_user_mac and row['User ID'] == current_user_id and row['AP Name'] == current_ap_name:
        continue
    else:
        connected_intervals.append({
            'User MAC Address': current_user_mac,
            'User ID': current_user_id,
            'AP Name': current_ap_name,
            'Time Start': current_start_time,
            'Time End': row['Time']
        })
        current_user_mac = row['User MAC Address']
        current_user_id = row['User ID']
        current_ap_name = row['AP Name']
        current_start_time = row['Next_Time']

# Create a DataFrame from the connected intervals
connected_intervals_df = pd.DataFrame(connected_intervals)

# Drop duplicates and reset the index
connected_intervals_df = connected_intervals_df.drop_duplicates().reset_index(drop=True)

# Save the result to a new Excel file with datetime formatting
connected_intervals_df.to_excel("connected_intervals.xlsx", index=False)

# Display the resulting DataFrame
print(connected_intervals_df)
