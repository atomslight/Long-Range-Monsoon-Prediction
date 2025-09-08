# Step 1: Read data from Excel file into DataFrame
df = pd.read_excel('inputdata3.xlsx')
df.columns = ['Year', 'Date', 'Precipitation']

# Step 2: Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Step 3: Extract year and month from dates
df['Month'] = df['Date'].dt.month

# Step 4: Find the greatest value of precipitation for each month
monthly_max_precipitation = df.groupby(['Year', 'Month'])['Precipitation'].max().unstack()
# Step 5: Add a column for sum and average of the first 12 months

monthly_max_precipitation['13 (Avg)'] = monthly_max_precipitation.iloc[:, :12].mean(axis=1)
# Step 5: Write results to another Excel file
monthly_max_precipitation.to_excel('monthly_max_precipitation.xlsx')
