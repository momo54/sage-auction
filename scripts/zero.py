import pandas as pd

# Charger les données depuis un fichier CSV
df = pd.read_csv('results/final.csv', names=['Query', 'Approach', 'Instance', 'ExecutionTime', 'ResultsCount'])

# Filtrer pour trouver les requêtes qui retournent 0 résultats
zero_results = df[df['ResultsCount'] == 0]

print(zero_results)

# Extraire les identifiants uniques de ces requêtes
unique_queries = zero_results['Query'].unique()

print("Requêtes qui retournent 0 résultats :", unique_queries)
