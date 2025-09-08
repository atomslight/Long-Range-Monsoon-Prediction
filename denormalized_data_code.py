import pandas as pd
import numpy as np

# Read data from Excel file
df = pd.read_excel("dataset.xlsx")

# Extract parameter names
parameters = df["PARAMETER"].unique()

# Define a function to normalize the dataset values using Equation 1
def normalize_data(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val)
    return min_val, max_val, normalized_data

# Normalize each parameter's dataset using Equation 1
normalized_data = {}
for parameter in parameters:
    parameter_data = df[df["PARAMETER"] == parameter].iloc[:, 2:-1]  # Exclude "PARAMETER" and "YEAR" columns
    min_val, max_val, norm_data = normalize_data(parameter_data)
    normalized_data[parameter] = {"min_val": min_val, "max_val": max_val, "normalized_data": norm_data}

# Define a function to denormalize the dataset values using Equation 2
def denormalize_data(min_val, max_val, normalized_data):
    print("MIN VAL",min_val)
    denormalized_data = (min_val - normalized_data * max_val) / (normalized_data - 1)
    return denormalized_data

# Denormalize each parameter's dataset using Equation 2
denormalized_data = {}
for parameter, data in normalized_data.items():
    min_val = data["min_val"]
    max_val = data["max_val"]
    norm_data = data["normalized_data"]
    denorm_data = denormalize_data(min_val, max_val, norm_data)
    denormalized_data[parameter] = denorm_data

# Write denormalized dataset values to a new Excel file
denormalized_output_file = "denormalized_data_equation2.xlsx"
with pd.ExcelWriter(denormalized_output_file) as writer:
    for parameter, data in denormalized_data.items():
        pd.DataFrame(data).to_excel(writer, sheet_name=parameter)

print("Denormalized dataset values saved to:", denormalized_output_file)
