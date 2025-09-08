import pandas as pd
import matplotlib.pyplot as plt

# Data for model development period (1993-2011)
data_model_development = {
    'YEAR': [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011],
    'Predicted TMRF': [282.222756, 207.1296221, 235.5963818, 201.3775961, 306.1560541, 63.86441677, 147.5526323, 183.1022896, 150.2656673, 
                       202.6334328, 247.2671218, 115.590751, 169.6282409, 116.5973991, 120.213308, 142.1411774, 173.4021575, 182.0056715, 
                       86.18304181],
    'Actual TMRF': [171.09, 172.18, 158.02, 162.78, 161.55, 119.61, 125.12, 160, 138.7, 162.36, 160.41, 130.91, 166.44, 188.44, 
                    135.25, 143.7, 168.62, 150.2, 177.81]
}

# Data for testing period (2012-2023)
data_testing = {
    'YEAR': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'Predicted TMRF': [106.8721515, 158.8956957, 184.8759347, 201.5845687, 219.8377412, 249.6307468, 111.8397294, 130.5976688, 237.3531188, 
                       193.8086227, 134.9286848, 132.5281656],
    'Actual TMRF': [95.15, 157.33, 140.83, 174.17, 192.54, 165.97, 100.61, 136.74, 200.57, 113.9, 108.43, 147.93]
}

# Create DataFrames
df_model_development = pd.DataFrame(data_model_development)
df_testing = pd.DataFrame(data_testing)

# Combine the DataFrames
combined_data = pd.concat([df_model_development, df_testing])

# Plot the graph
plt.figure(figsize=(14, 7))
plt.plot(combined_data['YEAR'], combined_data['Actual TMRF'], marker='o', linestyle='-', color='black', label='Actual')
plt.plot(combined_data['YEAR'], combined_data['Predicted TMRF'], marker='x', linestyle='--', color='brown', label='Predicted')

# Highlight the model development and testing periods
plt.axvline(x=2011, color='gray', linestyle='--')
plt.text(2002, plt.ylim()[1] - 10, 'Model Development Period', horizontalalignment='center', verticalalignment='center', rotation=90, fontsize=8)
plt.text(2017, plt.ylim()[1] - 10, 'Testing Period', horizontalalignment='center', verticalalignment='center', rotation=90, fontsize=8)

# Highlight verification for 2023
plt.axvline(x=2023, color='gray', linestyle='--')
plt.text(2023, plt.ylim()[1] - 10, 'Verification\nfor 2023', horizontalalignment='center', verticalalignment='center', rotation=90, fontsize=8)

# Add titles and labels
plt.title('PERFORMANCE OF MODEL IN DEVELOPMENT AND VALIDATION PERIOD')
plt.xlabel('YEAR')
plt.ylabel('TMRF')
plt.legend()

# Set x-axis to show every year from 1993 to 2023
plt.xticks(ticks=combined_data['YEAR'], labels=combined_data['YEAR'], rotation=45)

# Save the plot as output.png
plt.savefig('output.png')

# Show plot
plt.show()
