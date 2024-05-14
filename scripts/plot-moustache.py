import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données depuis un fichier CSV
df = pd.read_csv('results/final.csv', names=['Query', 'Approach', 'Instance', 'ExecutionTime', 'ResultsCount'])

# Calculer les moyennes par requête et par approche
mean_stats = df.groupby(['Query', 'Approach']).ExecutionTime.mean().reset_index(name='AverageExecutionTime')

# Préparer le graphique
plt.figure(figsize=(12, 8))
ax = sns.boxplot(data=mean_stats, x='Approach', y='AverageExecutionTime')

# Mettre l'axe des Y en échelle logarithmique
ax.set_yscale('log')

plt.title('Distribution of Average Execution Times by Approach')
plt.xlabel('Approach')
plt.ylabel('Average Execution Time (log scale)')
plt.xticks(rotation=45)  # Fait tourner les labels des abscisses pour une meilleure lisibilité
plt.grid(True)

# Sauvegarder le graphique dans un fichier
plt.savefig('results/plot-moustache.png', format='png', dpi=300)

# Afficher le graphique à l'écran (optionnel)
plt.show()

# Fermer le plot pour libérer la mémoire
plt.close()
