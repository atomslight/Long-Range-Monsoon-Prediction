import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Step 1: Load normalized data from Excel file
def load_data(file_path):
    df = pd.read_excel(file_path)
    # Extract the 12 input parameters and TMRF (target)
    data = df.iloc[:, 1:14].values
    return data[:, :-1], data[:, -1]  # Return input parameters and target separately

def train_model(data, target, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, momentum, epochs):
    velocity_hidden_weights = tf.zeros_like(hidden_layer_weights)
    velocity_hidden_bias = tf.zeros_like(hidden_layer_bias)
    velocity_output_weights = tf.zeros_like(output_layer_weights)
    velocity_output_bias = tf.zeros_like(output_layer_bias)
    
    for epoch in range(epochs):
        for i in range(len(data)):
            x = data[i]
            x = tf.expand_dims(x, 0)  # Make x a 1x12 matrix
            y_true = tf.constant([target[i]], dtype=tf.float64)

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

    return hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias

def predict(data, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias):
    predictions = []
    for i in range(len(data)):
        x = data[i]
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
def output_results(predictions, y_true, mad, sd, cc, mse):
    # Create a DataFrame for predictions
    df_predictions = pd.DataFrame({'Predicted TMRF': predictions.flatten(), 'True TMRF': y_true.flatten()})
    df_predictions.to_excel('predictions.xlsx', index=False)
    print("Predictions saved to predictions.xlsx")
    
    # Create a DataFrame for metrics
    df_metrics = pd.DataFrame({'MAD': [mad], 'SD': [sd], 'CC': [cc], 'MSE': [mse]})
    df_metrics.to_excel('metrics.xlsx', index=False)
    print("Metrics saved to metrics.xlsx")

def main():
    # Load data
    data, target = load_data('normalized_data.xlsx')

    # Split the data into training and testing sets (80% train, 20% test)
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2, random_state=42)

    # Set hyperparameters
    learning_rate = 0.0364438
    momentum = 1.0
    epochs = 5000

    # Define weights and biases with specified values
    hidden_layer_weights = np.array([
      [0.476859047461376, 0.869962417128569, 0.646818460327561],
      [0.335570830864129, 0.351934880435176, 0.0166089883392408],
      [0.588218197754366, 0.785998391651733, 0.0597466266275366],
      [0.67152784503857, 0.0133760085835681, 0.420916913961882],
      [0.193541797418661, 0.638741120654357, 0.41264796554717],
      [0.798026063297586, 0.884907019754901, 0.365214445923793],
      [0.114825985328528, 0.00919485999726644, 0.88564099282692],
      [0.290092186490632, 0.666791367032787, 0.726272649790377],
      [0.973104416006657, 0.651048852661124, 0.915417554170822],
      [0.284370094901216, 0.339418757312569, 0.903559129854485],
      [0.307924984052735, 0.310681108033961, 0.159641405303369],
      [0.95824137427446, 0.182192077544901, 0.270966858566609]
    ], dtype=np.float64)
    
    hidden_layer_bias = np.array([0.367257689828437, 0.204492956574989, 0.00664597413608115], dtype=np.float64)
    
    output_layer_weights = np.array([[0.70355485433932],
                                     [0.27076991785223],
                                     [0.581742969532814]], dtype=np.float64)
    
    output_layer_bias = np.array([0.445260738677795], dtype=np.float64)

    # Train the model
    hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias = train_model(
        data_train, target_train, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias, learning_rate, momentum, epochs
    )

    # Make predictions on the test data
    predictions = predict(data_test, hidden_layer_weights, hidden_layer_bias, output_layer_weights, output_layer_bias)

    # Calculate metrics
    y_true = target_test  # Use the test target values
    mad, sd, cc, mse = calculate_metrics(y_true, predictions)

    # Output results
    output_results(predictions, y_true, mad, sd, cc, mse)

if __name__ == "__main__":
    main()
