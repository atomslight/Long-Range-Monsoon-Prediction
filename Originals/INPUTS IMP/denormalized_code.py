import pandas as pd
import numpy as np

# Read data from Excel file for TMRF
df_tmrf = pd.read_excel("TMRF.xlsx")

# Read data from Excel file for ri
df_ri = pd.read_excel("predictions.xlsx")

# Define the single parameter
parameter = "Heaviest Rainfall in 24 hour HYRF"

# Select "JUNE", "JULY", "AUGUST", "SEPTEMBER" columns for min and max calculations from TMRF file
monthly_data = df_tmrf[["JUNE", "JULY", "AUGUST", "SEPTEMBER"]]

# Calculate min and max values for each year
min_val = monthly_data.min(axis=1).values
max_val = monthly_data.max(axis=1).values

# Extract the 'TMRF' values (Xi)
xi_values = df_tmrf["TMRF"].values

# Extract 'ri' values from the second column

ri_values = df_ri["True TMRF"].values


# Define a function to denormalize the dataset values using Equation 2
def denormalize_data(xi, min_val, max_val, ri):
    print(xi)
    denormalized_data = ((min_val - ri*max_val) / (ri - 1))
    return denormalized_data

# Apply the denormalization
denormalized_values = denormalize_data(xi_values, min_val, max_val, ri_values)

# Create a DataFrame for the denormalized data
denormalized_df = pd.DataFrame({
    "YEAR": df_tmrf["YEAR"],
    "TMRF": denormalized_values
})

# Write denormalized dataset values to a new Excel file
output_file = "TMRF_denormalized_data_equation2.xlsx"
with pd.ExcelWriter(output_file) as writer:
    denormalized_df.to_excel(writer, sheet_name=parameter[:31], index=False)

print("Denormalized dataset values saved to:", output_file)
