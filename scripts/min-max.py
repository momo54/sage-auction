import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv('results/final.csv', names=['Query', 'Approach', 'Instance', 'ExecutionTime', 'ResultsCount'])

# Filtrer les données pour l'approche 'bid'
bid_data = df[df['Approach'] == 'bid']

# Calculer le nombre maximal, minimal et moyen de résultats
max_results = bid_data['ResultsCount'].max()
min_results = bid_data['ResultsCount'].min()
mean_results = bid_data['ResultsCount'].mean()

print("Nombre maximal de résultats pour l'approche 'bid':", max_results)
print("Nombre minimal de résultats pour l'approche 'bid':", min_results)
print("Nombre moyen de résultats pour l'approche 'bid':", mean_results)
