import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Step 1: Load normalized data from Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    data = df['Average'].values
    return data

# Step 2: Load weights and biases from Excel file
def load_weights(file_path):
    df = pd.read_excel(file_path, header=None)
    hidden_layer_weights = df.iloc[0:12, 0:3].values
    hidden_layer_bias = df.iloc[7, 0:3].values
    output_layer_weights = df.iloc[11, 0:3].values.reshape(3, 1)
    output_layer_bias = df.iloc[12, 0]
    return hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias

# Step 3: Train the model using the Delta rule
def train_model(data, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, epochs):
    for epoch in range(epochs):
        for i in range(len(data) - 12):
            x = data[i:i+12]
            y_true = data[i+12]

            # Forward pass
            hidden_layer_input = np.dot(x, hidden_layer_weights) + hidden_layer_bias
            hidden_layer_output = 1 / (1 + np.exp(-hidden_layer_input))

            output_layer_input = np.dot(hidden_layer_output, output_layer_weights) + output_layer_bias
            y_pred = 1 / (1 + np.exp(-output_layer_input))

            # Backward pass (Delta rule)
            output_error = y_true - y_pred
            output_delta = output_error * (y_pred * (1 - y_pred))

            hidden_error = output_delta.dot(output_layer_weights.T)
            hidden_delta = hidden_error * (hidden_layer_output * (1 - hidden_layer_output))

            # Update weights and biases
            output_layer_weights += learning_rate * hidden_layer_output.reshape(-1, 1).dot(output_delta.reshape(1, -1))
            output_layer_bias += learning_rate * output_delta

            hidden_layer_weights += learning_rate * x.reshape(-1, 1).dot(hidden_delta.reshape(1, -1))
            hidden_layer_bias += learning_rate * hidden_delta

    # Final predictions
    predictions = []
    for i in range(len(data) - 12, len(data)):
        x = data[i:i+12]
        hidden_layer_input = np.dot(x, hidden_layer_weights) + hidden_layer_bias
        hidden_layer_output = 1 / (1 + np.exp(-hidden_layer_input))

        output_layer_input = np.dot(hidden_layer_output, output_layer_weights) + output_layer_bias
        y_pred = 1 / (1 + np.exp(-output_layer_input))
        predictions.append(y_pred)

    return np.array(predictions).flatten()

# Step 4: Calculate metrics: MAD, SD, CC, MSE
def calculate_metrics(y_true, y_pred):
    mad = np.mean(np.abs(y_true - y_pred))
    sd = np.sqrt(np.mean((y_true - np.mean(y_true)) ** 2))
    cc = np.corrcoef(y_true, y_pred.flatten())[0, 1]
    mse = np.mean((y_true - y_pred) ** 2)
    return mad, sd, cc, mse

# Step 5: Output the predicted target values and metrics
def output_results(predictions, mad, sd, cc, mse):
    df_results = pd.DataFrame({'Predicted Target': predictions.flatten(), 'MAD': [mad], 'SD': [sd], 'CC': [cc], 'MSE': [mse]})
    df_results.to_excel('output_results.xlsx', index=False)
    print("Output results saved to output_results.xlsx")

# Main function
def main():
    # Load data and weights
    data = load_data('normalized_data.xlsx')
    hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias = load_weights('random_weights.xlsx')

    # Set hyperparameters
    learning_rate = 0.3
    epochs = 5000000

    # Train the model
    predictions = train_model(data, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, epochs)

    # Calculate metrics
    y_true = data[12:]
    mad, sd, cc, mse = calculate_metrics(y_true, predictions)

    # Output results
    output_results(predictions, mad, sd, cc, mse)

if __name__ == "__main__":
    main()
