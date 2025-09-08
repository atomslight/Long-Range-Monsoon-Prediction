import pandas as pd

# Load the Excel file
file_path = 'normalized_data_till_2011.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Pivot the dataframe
df_pivot = df.pivot_table(index='YEAR', columns='Parameter', values='Average')

# Flatten the columns and rename them to include "Average of"
df_pivot.columns = [f'{param}' for param in df_pivot.columns]

# Print out the actual column names in the pivoted DataFrame
print("Actual columns after pivoting:")
print(df_pivot.columns)

# Specify the desired order of columns
desired_order = [
    'Highest Maximum Temperature T2M_MAX',
    'Lowest Minimum Temperature',
    'Mean Maximum Temperature MT2M_MAX',
    'Mean Minimum Temperature',
    'Mean Relative Humidity',
    'Mean Wind Speed',
    'Mean Station Level Pressure PS',
    'Mean Dew T2MDEW',
    'Mean Wet Bulb',
    'Mean Vapour Pressure VP',
    'Heaviest Rainfall in 24 hour HYRF',
    'Cloud Amt'
]

# Create a new list of column names in the desired order
ordered_columns = [f'{param}' for param in desired_order]

# Check for any missing columns
missing_columns = [col for col in ordered_columns if col not in df_pivot.columns]
if missing_columns:
    print("The following columns are missing in the DataFrame:")
    print(missing_columns)
else:
    # Reorder the columns
    df_pivot = df_pivot[ordered_columns]

    # Reset the index to have 'YEAR' as a column
    df_pivot.reset_index(inplace=True)

    # Save the transformed dataframe to a new Excel file
    output_file_path = 'transformed_data.xlsx'  # Replace with your desired output file path
    df_pivot.to_excel(output_file_path, index=False)

    print(f"Transformed data has been saved to {output_file_path}")
