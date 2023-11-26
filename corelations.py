import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Step 3: Read CSV File
df = pd.read_csv('df1_cleaned_final.csv')
df = df[:10]
# Step 4: One-hot encode categorical columns and Compute Correlation
df_encoded = pd.get_dummies(df)
correlation_matrix = df_encoded.corr()

# Step 5: Display Correlation Matrix
print(correlation_matrix)

# Visualize Correlation Matrix as a Heatmap
plt.figure(figsize=(60, 50))
heatmap = sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# Save the plot in highest quality (adjust the filename and format as needed)
heatmap.get_figure().savefig('correlation_matrix.png', bbox_inches='tight', dpi=300)