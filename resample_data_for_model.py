import pandas as pd

# Load your DataFrame
df = pd.read_csv('df1_with_datetime.csv')

# Step 1: Convert 'datetime' column to the DataFrame index
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
# Step 1: Group by 'datetime' and 'city' and count rows
grouped_df = df.groupby(['datetime', 'city']).size().reset_index(name='count')

# Step 2: Create a new DataFrame with unique date and city combinations and counts
unique_dates_cities_df = grouped_df.copy()

# Filter the DataFrame for 'Mumbai' city
# mumbai_details = unique_dates_cities_df[unique_dates_cities_df['city'] == 'mumbai']

# print(mumbai_details)
print(unique_dates_cities_df)
unique_dates_cities_df.to_csv('unique_dates_cities_df.csv')