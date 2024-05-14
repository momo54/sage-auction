import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données depuis un fichier CSV
df = pd.read_csv('results/final.csv', names=['Query', 'Approach', 'Instance', 'ExecutionTime', 'ResultsCount'])

# Calculer les moyennes et nommer explicitement la colonne de moyenne
mean_stats = df.groupby(['Query', 'Approach']).ExecutionTime.mean().reset_index(name='AverageExecutionTime')

# Fusionner les données triées par les temps moyens de 'bid'
sorted_queries = mean_stats[mean_stats['Approach'] == 'bid'].sort_values('AverageExecutionTime')
mean_stats = pd.merge(sorted_queries[['Query']], mean_stats, on='Query')

# Préparer le graphique
plt.figure(figsize=(12, 8))
sns.lineplot(data=mean_stats, x='Query', y='AverageExecutionTime', hue='Approach', marker='o')

# Mettre l'axe des Y en échelle logarithmique
plt.yscale('log')

# Cacher les étiquettes sur l'axe des X pour ne pas afficher les noms des requêtes
plt.xticks([])
plt.xlabel('Queries (names hidden)')

plt.title('Average Execution Time by Approach')
plt.ylabel('Average Execution Time (log scale)')
plt.legend(title='Approach')
plt.grid(True)
plt.tight_layout()
#plt.show()
# Sauvegarder le graphique dans un fichier
plt.savefig('results/plot-curve.png', format='png', dpi=300)
