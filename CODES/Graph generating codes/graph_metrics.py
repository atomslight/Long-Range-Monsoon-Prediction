import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Prepare the data
metrics = {
    'Metric': ['MAD', 'SD', 'CC', 'MSE'],
    'Value': [0.027861576, 0.047373332, 0.83002909, 0.001229107]
}

# Convert to DataFrame
metrics_df = pd.DataFrame(metrics)

# Step 2: Plot the data
plt.figure(figsize=(8, 6))
plt.bar(metrics_df['Metric'], metrics_df['Value'], color='skyblue')
plt.title('Metrics')
plt.ylabel('Value')
plt.xlabel('Metric')

# Save the plot to a file
plt.savefig('metrics_plot.png')

# Display the plot
plt.show()
