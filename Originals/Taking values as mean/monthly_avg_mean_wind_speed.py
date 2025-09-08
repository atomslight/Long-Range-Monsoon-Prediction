import pandas as pd

# Step 1: Read data from Excel file into DataFrame
df = pd.read_excel('datainput.xlsx')

# Step 2: Convert DOY column to date format
df['Date'] = pd.to_datetime(df['DOY'], format='%d-%m-%Y')

# Step 3: Extract year and month from dates
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Step 4: Calculate average T2M_MAX for each month within each year
monthly_avg = df.groupby(['Year', 'Month'])['WS2M'].mean().unstack()

# Step 5: Add a column for sum and average of the first 12 months

monthly_avg['13 (Avg)'] = monthly_avg.iloc[:, :12].mean(axis=1)

# Step 6: Write results to another Excel file
monthly_avg.to_excel('monthly_avg_mean_wind_speed.xlsx')