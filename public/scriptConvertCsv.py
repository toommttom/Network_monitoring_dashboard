import pandas as pd

# Charger le fichier XLSX
xlsx_file = "C:/Users/Tom/Documents/ecole/INGE 3TD/projets/network_mon_dash/backend/app/data/Trace/data_tracesV2-P1.xlsx"  # Remplace par le nom de ton fichier
df = pd.read_excel(xlsx_file)

# Sauvegarder en CSV
csv_file = "C:/Users/Tom/Documents/ecole/INGE 3TD/projets/network_mon_dash/backend/app/data/Trace/data_tracesV2-P1.csv"  # Nom du fichier CSV de sortie
df.to_csv(csv_file, index=False, encoding="utf-8")  # index=False pour ne pas ajouter de colonne d’index

print(f"Le fichier a été converti et sauvegardé sous {csv_file}")