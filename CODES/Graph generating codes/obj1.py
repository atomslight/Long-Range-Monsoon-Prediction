import numpy as np
import matplotlib.pyplot as plt

# Synthetic data for example purposes
epochs = np.arange(1, 21)
training_loss = np.random.uniform(0.01, 0.05, size=20)
validation_loss = np.random.uniform(0.02, 0.06, size=20)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(epochs, training_loss, label='Training Loss', marker='o')
plt.plot(epochs, validation_loss, label='Validation Loss', marker='o')
plt.title('Training and Validation Loss of Neural Network on Weather Data Time Series')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Save the plot to a file
plt.savefig('deep_learning_weather_loss.png')

# Show the plot
plt.show()
