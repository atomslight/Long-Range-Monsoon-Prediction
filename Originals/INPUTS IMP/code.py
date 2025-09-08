import pandas as pd
import numpy as np
import tensorflow as tf

# Step 1: Load normalized data from a single Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    data = {}
    for year in df['YEAR'].unique():
        year_data = df[df['YEAR'] == year].iloc[:, 1:].values  # Exclude the 'YEAR' column
        data[year] = year_data
    return data

def generate_random_weights(input_size, hidden_size, output_size):
    # Generate random weights and biases for the hidden layer
    hidden_layer_weights = tf.random.uniform(shape=(input_size, hidden_size), minval=0, maxval=1, dtype=tf.float64)
    hidden_layer_bias = tf.random.uniform(shape=(hidden_size,), minval=0, maxval=1, dtype=tf.float64)
    
    # Generate random weights and bias for the output layer
    output_layer_weights = tf.random.uniform(shape=(hidden_size, output_size), minval=0, maxval=1, dtype=tf.float64)
    output_layer_bias = tf.random.uniform(shape=(output_size,), minval=0, maxval=1, dtype=tf.float64)
    
    # Save weights and biases to Excel file
    with pd.ExcelWriter('random_weights.xlsx') as writer:
        pd.DataFrame(hidden_layer_weights.numpy()).to_excel(writer, sheet_name='HiddenLayerWeights', index=False)
        pd.DataFrame(hidden_layer_bias.numpy()).to_excel(writer, sheet_name='HiddenLayerBias', index=False)
        pd.DataFrame(output_layer_weights.numpy()).to_excel(writer, sheet_name='OutputLayerWeights', index=False)
        pd.DataFrame(output_layer_bias.numpy()).to_excel(writer, sheet_name='OutputLayerBias', index=False)
    
    return hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias

def train_model(data, target, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, momentum, epochs):
    input_size = hidden_layer_weights.shape[0]  # Number of features in input window
    hidden_size = hidden_layer_weights.shape[1] # Number of neurons in hidden layer
    output_size = output_layer_weights.shape[1] # Number of output neurons
    
    velocity_hidden_weights = tf.zeros_like(hidden_layer_weights)
    velocity_hidden_bias = tf.zeros_like(hidden_layer_bias)
    velocity_output_weights = tf.zeros_like(output_layer_weights)
    velocity_output_bias = tf.zeros_like(output_layer_bias)
    
    for epoch in range(epochs):
        for i in range(len(data) - input_size):
            x = data[i:i+input_size]
            x = tf.expand_dims(x, 0)  # Make x a 1x12 matrix
            y_true = tf.constant([target[i+input_size]], dtype=tf.float64)

            # Forward pass
            hidden_layer_input = tf.linalg.matmul(x, hidden_layer_weights) + hidden_layer_bias
            hidden_layer_output = tf.nn.sigmoid(hidden_layer_input)

            output_layer_input = tf.linalg.matmul(hidden_layer_output, output_layer_weights) + output_layer_bias  
            y_pred = tf.nn.sigmoid(output_layer_input)

            # Backward pass (Delta rule)
            output_error = y_true - y_pred
            output_delta = output_error * y_pred * (1 - y_pred)

            hidden_error = tf.linalg.matmul(output_delta, tf.transpose(output_layer_weights))
            hidden_delta = hidden_error * hidden_layer_output * (1 - hidden_layer_output)

            # Update weights and biases with momentum
            velocity_output_weights = momentum * velocity_output_weights + learning_rate * tf.linalg.matmul(tf.transpose(hidden_layer_output), output_delta)
            velocity_output_bias = momentum * velocity_output_bias + learning_rate * output_delta

            velocity_hidden_weights = momentum * velocity_hidden_weights + learning_rate * tf.linalg.matmul(tf.transpose(x), hidden_delta)
            velocity_hidden_bias = momentum * velocity_hidden_bias + learning_rate * hidden_delta

            output_layer_weights += velocity_output_weights
            output_layer_bias += velocity_output_bias

            hidden_layer_weights += velocity_hidden_weights
            hidden_layer_bias += velocity_hidden_bias

    # Final predictions
    predictions = []
    for i in range(len(data) - input_size):
        x = data[i:i+input_size]
        x = tf.expand_dims(x, 0)  # Make x a 1x12 matrix
        hidden_layer_input = tf.linalg.matmul(x, hidden_layer_weights) + hidden_layer_bias  
        hidden_layer_output = tf.nn.sigmoid(hidden_layer_input)

        output_layer_input = tf.linalg.matmul(hidden_layer_output, output_layer_weights) + output_layer_bias  
        y_pred = tf.nn.sigmoid(output_layer_input)
        predictions.append(y_pred.numpy().flatten())

    return np.array(predictions).flatten()

# Step 4: Calculate metrics: MAD, SD, CC, MSE
def calculate_metrics(y_true, y_pred):
    mad = np.mean(np.abs(y_true - y_pred))
    sd = np.sqrt(np.mean((y_true - np.mean(y_true)) ** 2))
    cc = np.corrcoef(y_true, y_pred.flatten())[0, 1]
    mse = np.mean((y_true - y_pred) ** 2)
    return mad, sd, cc, mse

# Step 5: Output the predicted target values and metrics
def output_results(predictions, y_true, mad, sd, cc, mse, year):
    # Create a DataFrame for predictions
    df_predictions = pd.DataFrame({'Predicted Target': predictions.flatten(), 'True Target': y_true.flatten()})
    df_predictions.to_excel(f'predictions_{year}.xlsx', index=False)
    print(f"Predictions saved to predictions_{year}.xlsx")
    
    # Create a DataFrame for metrics
    df_metrics = pd.DataFrame({'MAD': [mad], 'SD': [sd], 'CC': [cc], 'MSE': [mse]})
    df_metrics.to_excel(f'metrics_{year}.xlsx', index=False)
    print(f"Metrics saved to metrics_{year}.xlsx")

def main():
    # Load data
    data = load_data('Normalized Average of 12 parameters Yearwise.xlsx')

    # Set hyperparameters
    learning_rate = 0.3
    momentum = 1.0
    epochs = 500

    # Generate random weights and biases
    input_size = 12
    hidden_size = 3
    output_size = 1

    for year, year_data in data.items():
        print("Training model for year:", year)
        target = year_data[:, -1]  # Target TMRF values for the year
        year_data = year_data[:, :-1]  # Input parameters for the year

        # Generate random weights and biases for the year
        hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias = generate_random_weights(input_size, hidden_size, output_size)

        # Train the model for the year
        predictions = train_model(year_data, target, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, momentum, epochs)

        # Calculate metrics for the year
        y_true = target
        mad, sd, cc, mse = calculate_metrics(y_true, predictions)

        # Output results for the year
        output_results(predictions, y_true, mad, sd, cc, mse, year)

if __name__ == "__main__":
    main()
