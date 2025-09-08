import pandas as pd
import numpy as np

# Read data from Excel file
df = pd.read_excel("TMRF.xlsx")

# Define the single parameter
parameter = "Heaviest Rainfall in 24 hour HYRF"

# Filter data for the specific parameter
parameter_df = df[df["PARAMETER"] == parameter]

# Select "JUNE", "JULY", "AUGUST", "SEPTEMBER" columns for min and max calculations
monthly_data = parameter_df[["JUNE", "JULY", "AUGUST", "SEPTEMBER"]]

# Calculate min and max values for each year
min_val = monthly_data.min(axis=1)
max_val = monthly_data.max(axis=1)

# Extract the 'TMRF' values (Xi)
xi_values = parameter_df["TMRF"]

# Define a function to normalize the dataset values using Equation 1
def normalize_data(xi, min_val, max_val):
    normalized_data = (xi + min_val) / (xi + max_val)
    return normalized_data

# Apply the normalization
normalized_values = normalize_data(xi_values, min_val, max_val)

# Create a DataFrame for the normalized data
normalized_df = pd.DataFrame({
    "YEAR": parameter_df["YEAR"],
    "TMRF": normalized_values
})

# Write normalized dataset values to a new Excel file
output_file = "TMRF_normalized_data_equation1_new.xlsx"
with pd.ExcelWriter(output_file) as writer:
    normalized_df.to_excel(writer, sheet_name=parameter[:31], index=False)

print("Normalized dataset values saved to:", output_file)
