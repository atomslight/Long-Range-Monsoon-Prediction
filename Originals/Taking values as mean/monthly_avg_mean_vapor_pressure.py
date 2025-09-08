import pandas as pd

# Step 1: Read data from Excel file into DataFrame
df = pd.read_excel('datainput1.xlsx')

# Step 2: Convert DOY column to date format
df['Date'] = pd.to_datetime(df['DOY'], format='%d-%m-%Y')

# Step 3: Extract year and month from dates
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Step 4: Calculate vapor pressure using specific humidity and temperature
# Assuming QV2M is specific humidity in g/kg and T2M is temperature in Celsius
# Clausius-Clapeyron equation: e = 6.112 * exp((17.67 * T) / (T + 243.5)) * (Q / (0.622 + Q)) * 10
# where e is vapor pressure in hPa, T is temperature in Celsius, and Q is specific humidity in kg/kg
# Convert QV2M from g/kg to kg/kg
df['QV2M_kg/kg'] = df['QV2M'] / 1000
# Calculate vapor pressure using Clausius-Clapeyron equation
df['vapor_pressure'] = 6.112 * (10 ** ((17.67 * df['T2M']) / (df['T2M'] + 243.5))) * (df['QV2M_kg/kg'] / (0.622 + df['QV2M_kg/kg']))

# Step 5: Calculate mean vapor pressure for each month within each year
monthly_avg_vapor_pressure = df.groupby(['Year', 'Month'])['vapor_pressure'].mean().unstack()

# Step 6: Add a column for sum and average of the first 12 months
monthly_avg_vapor_pressure['13 (Avg)'] = monthly_avg_vapor_pressure.iloc[:, :12].mean(axis=1)

# Step 7: Write results to another Excel file
monthly_avg_vapor_pressure.to_excel('monthly_avg_mean_vapor_pressure.xlsx')
