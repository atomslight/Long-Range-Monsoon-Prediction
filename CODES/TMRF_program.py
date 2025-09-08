import pandas as pd

# Read the Excel file
file_path = 'TMRF_input.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Display the DataFrame to understand its structure
print("Initial DataFrame:")
print(df)

# Extract the specific rows and columns needed
# Assuming the first row contains headers and the data starts from the second row
# Extracting relevant columns
df_filtered = df.iloc[:, :6]  # Select columns up to September

# Rename columns for easier access
df_filtered.columns = ['PARAMETER', 'YEAR', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER']

# Calculate TMRF by summing the four months data
df_filtered['TMRF'] = df_filtered[['JUNE', 'JULY', 'AUGUST', 'SEPTEMBER']].sum(axis=1)

# Output the resulting DataFrame
print("DataFrame with TMRF:")
print(df_filtered)

# If needed, save the result back to an Excel file
output_file_path = 'output_with_tmrf.xlsx'
df_filtered.to_excel(output_file_path, index=False)
