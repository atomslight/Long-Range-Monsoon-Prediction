import pandas as pd
import numpy as np

# Read data from Excel file
df = pd.read_excel("dataset.xlsx")

# Extract parameter names
parameters = [
    "Highest Maximum Temperature T2M_MAX",
    "Lowest Minimum Temperature T2M_MIN",
    "Mean Maximum Temperature MT2M_MAX",
    "Mean Minimum Temperature MT2M_MIN",
    "Mean Relative Humidity RH2M",
    "Mean Wind Speed WS2M",
    "Mean Station Level Pressure PS",
    "Mean Dew T2MDEW",
    "Mean Wet Bulb T2MWET",
    "Mean Vapour Pressure VP",
    "Heaviest Rainfall in 24 hour HYRF",
    "CLOUD_AMT"
]

# Define a function to normalize the dataset values using Equation 1
def normalize_data(xi, min_val, max_val):
    normalized_data = (xi + min_val) / (xi + max_val)
    return normalized_data

# Normalize each parameter's dataset using Equation 1
normalized_data = {}
for parameter in parameters:
    parameter_df = df[df["PARAMETER"] == parameter]  # Filter data for the current parameter
    monthly_data = parameter_df.iloc[:, 2:-1]  # Exclude "PARAMETER", "YEAR", and "ANN" columns
    min_val = monthly_data.min(axis=1)
    max_val = monthly_data.max(axis=1)
    xi_values = parameter_df["ANN"]
    normalized_values = normalize_data(xi_values, min_val, max_val)
    normalized_data[parameter[:31]] = pd.DataFrame({
        "YEAR": parameter_df["YEAR"],
        "ANN": normalized_values
    })

# Write normalized dataset values to a new Excel file
output_file = "normalized_data_equation1.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for parameter, data in normalized_data.items():
        data.to_excel(writer, sheet_name=parameter[:31], index=False)

print("Normalized dataset values saved to:", output_file)
