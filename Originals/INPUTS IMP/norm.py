import pandas as pd
# Step 1: Load normalized data from Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    # Extract the 12 input parameters and TMRF (target)
    data = df.iloc[:, 1:14].values
    print(data[:, :-1], data[:, -1])
    return data[:, :-1], data[:, -1]  # Return input parameters and target separately
def main():
    # Load data
    data, target = load_data('normalized_data.xlsx')
