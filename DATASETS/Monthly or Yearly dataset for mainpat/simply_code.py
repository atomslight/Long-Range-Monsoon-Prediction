import pandas as pd

# Step 1: Read data from Excel file into DataFrame
df = pd.read_excel('datainput.xlsx')

# Step 2: Convert DOY column to date format
df['Date'] = pd.to_datetime(df['DOY'], format='%d-%m-%Y')

# Step 3: Extract month from dates and group data by month
df['Month'] = df['Date'].dt.month

# Step 4: Calculate average T2M_MAX for each month
monthly_avg = df.groupby('Month')['T2M_MAX'].mean().reset_index()

# Step 5: Write results to another Excel file
monthly_avg.to_excel('monthly_avg_output.xlsx', index=False)
