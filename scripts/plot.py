import pandas as pd
import matplotlib.pyplot as plt

# Load data from a CSV file
data_df = pd.read_csv('results/final.csv', header=None, names=["Query", "Operation", "Flag", "ExecutionTime", "Count"])

# Pivot the data to have execution times for each operation type per query
pivot_data = data_df.pivot(index="Query", columns="Operation", values="ExecutionTime")

# Sort the queries by the execution time of the 'bid' operation
sorted_data = pivot_data.sort_values(by='bid')

# Preparing data for scatter plot
melted_data = sorted_data.reset_index().melt(id_vars='Query', var_name='Operation', value_name='ExecutionTime')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
operations = melted_data['Operation'].unique()
colors = plt.cm.get_cmap('tab10', len(operations))

# Plotting each operation type with a unique color
for i, operation in enumerate(operations):
    subset = melted_data[melted_data['Operation'] == operation]
#    ax.scatter(subset['Query'], subset['ExecutionTime'], color=colors(i), label=operation)
    ax.plot(subset['Query'], subset['ExecutionTime'], color=colors(i), label=operation)
ax.set_title('Execution Time by Operation Type, Sorted by Bid Time')
ax.set_xlabel('Query')
ax.set_ylabel('Execution Time (ms)')

# log scale
ax.set_yscale('log')

# Remove the x-axis labels
ax.set_xticklabels([])

plt.xticks(rotation=45)
plt.legend(title='Operation Type')
plt.tight_layout()
plt.show()
