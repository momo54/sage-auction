import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv('results/final.csv', names=['Query', 'Approach', 'Instance', 'ExecutionTime', 'ResultsCount'])

# Filtrer les données pour les approches 'rename-force-top20' et 'rename-force-500ms'
#filtered_data = df[df['Approach'].isin(['rename-force-top20', 'rename-force-500ms'])]

# Calculer les statistiques pour chaque approche
stats = df.groupby('Approach')['ResultsCount'].agg(['min', 'max', 'mean']).reset_index()

print(stats)
