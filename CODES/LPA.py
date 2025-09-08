import pandas as pd

# Load the Excel file
file_path = 'modified_file_actual.xlsx'
df = pd.read_excel(file_path)

# Assuming you have a column named 'LPA' which contains the Long Period Average values
# If not, replace 'LPA' with the column name that contains the LPA values
df['LPA'] = df['LPA'] * 31  # Multiply LPA by 31 to convert it to the same units as TMRF

# Perform the division and multiplication to calculate LPA in percentage
df['LPA_in_percentage'] = (df['TMRF'] / df['LPA']) * 100

# Save the modified DataFrame back to an Excel file
output_file_path = 'modified_file_actual_percentage.xlsx'
df.to_excel(output_file_path, index=False)

print(f"The modified data has been saved to {output_file_path}")
