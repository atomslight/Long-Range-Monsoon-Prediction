import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Synthetic data for example purposes
epochs = np.arange(1, 21)
training_loss = np.random.uniform(0.01, 0.06, size=20)
validation_loss = np.random.uniform(0.02, 0.06, size=20)

# Create the 3D plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot the training and validation loss
ax.plot(epochs, training_loss, zs=0, zdir='y', label='Training Loss', marker='o')
ax.plot(epochs, validation_loss, zs=1, zdir='y', label='Validation Loss', marker='o')

# Set labels and title
ax.set_title('Training and Validation Loss of Neural Network on Weather Data Time Series')
ax.set_xlabel('Epochs')
ax.set_ylabel('Loss Type')
ax.set_zlabel('Loss')
ax.set_yticks([0, 1])
ax.set_yticklabels(['Training', 'Validation'])

# Add legend
ax.legend()

# Show the plot
plt.show()

# Save the plot to a file
fig.savefig('deep_learning_weather_loss_3d.png')
