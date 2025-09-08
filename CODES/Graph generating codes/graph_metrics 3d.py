import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np

# Step 1: Prepare the data
metrics = {
    'Metric': ['MAD', 'SD', 'CC', 'MSE'],
    'Value': [0.027861576, 0.047373332, 0.83002909, 0.001229107]
}

# Convert to DataFrame
metrics_df = pd.DataFrame(metrics)

# Step 2: Plot the data
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Prepare data for the 3D bar plot
x = np.arange(len(metrics_df['Metric']))
y = np.zeros(len(metrics_df['Metric']))
z = metrics_df['Value']

# Plot bars
ax.bar(x, z, zs=y, zdir='y', color='darkblue')

# Set labels
ax.set_xlabel('Metric')
ax.set_ylabel('Y')
ax.set_zlabel('Value')

# Set tick labels for x-axis
ax.set_xticks(x)
ax.set_xticklabels(metrics_df['Metric'])

# Title
ax.set_title('3D Metrics')

# Save the plot to a file
plt.savefig('metrics_3d_plot.png')

# Display the plot
plt.show()
