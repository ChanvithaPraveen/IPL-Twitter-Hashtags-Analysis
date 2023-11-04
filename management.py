import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("f.csv")

# Exclude diagonal elements by setting them to NaN
for i in range(1, len(df.columns)):
    df.iat[i - 1, i] = float('NaN')

# Create a single figure for all pie charts
num_rows = len(df.columns) - 1
num_cols = len(df.columns) - 1

fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 12))


# Define a function to create a pie chart for a given cell
def create_pie_chart(ax, data, row_label, col_label):
    labels = ['Value', 'Average']
    values = [int(data), 7.5]  # Assuming an average of 7.5 based on your previous randomization logic

    ax.pie(values, labels=['', ''], autopct='', startangle=90)
    # ax.set_title(f'{row_label} vs {col_label}')
    ax.axis('equal')


# Create pie charts for each cell except diagonal elements
for i in range(1, len(df.columns)):
    for j in range(1, len(df.columns)):
        if i != j:
            row_label = df.columns[i]
            col_label = df.columns[j]
            cell_value = df.iat[i - 1, j]

            # Check if the cell has a valid value
            if not pd.isna(cell_value):
                create_pie_chart(axes[i - 1, j - 1], cell_value, row_label, col_label)

# Remove axis labels and ticks
for ax in axes.ravel():
    ax.set_xticks([])
    ax.set_yticks([])

# Add row and column names as annotations
for i, col_label in enumerate(df.columns[1:], start=0):
    axes[0, i].set_title(col_label, fontsize=12)
    axes[num_rows - 1, i].annotate(col_label, xy=(0.5, 1.1), xycoords='axes fraction', fontsize=12, ha='center')

for i, row_label in enumerate(df.columns[1:], start=0):
    axes[i, 0].annotate(row_label, xy=(-0.5, 0.5), xycoords='axes fraction', fontsize=12, ha='center')

# Adjust the layout and spacing
plt.tight_layout()

# Show the single figure with all pie charts
plt.show()