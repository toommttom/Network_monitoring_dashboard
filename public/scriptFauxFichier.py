import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Générer des données fictives similaires
num_rows = 50
base_latitude = 48.9607  # Latitude de Meaux
base_longitude = 2.8885  # Longitude de Meaux

data = {
    "Num_Test": range(1, num_rows + 1),
    "ID_user": ["Amour"] * num_rows,
    "Ville": ["MEAUX"] * num_rows,
    "Input": ["Midi"] * num_rows,
    "Technologie_Reseau": ["5G"] * num_rows,
    "Output": ["With headphones"] * num_rows,
    "Date_Performance": [datetime(2024, 11, 8, 16, 56, 45) + timedelta(seconds=i*5) for i in range(num_rows)],
    "Moment du ping": [datetime(2024, 11, 8, 16, 56, 50) + timedelta(seconds=i*5) for i in range(num_rows)],
    "Latence": np.random.uniform(50, 200, num_rows).round(2),
    "Jitter": np.random.uniform(0, 50, num_rows).round(2),
    "IP_source": ["192.168.229.241"] * num_rows,
    "server_name": ["Andre's UK Sound"] * num_rows,
    "IP_destination": ["139.162.251.38"] * num_rows,
    "Port_source": np.random.randint(50000, 65000, num_rows),
    "Port_destination": [22124] * num_rows,
    "PacketsLoss": np.zeros(num_rows),
    "Throuput": np.random.uniform(1000, 3000, num_rows).round(2),
    "Latitude": base_latitude + np.cumsum(np.random.uniform(-0.001, 0.001, num_rows)),
    "Longitude": base_longitude + np.cumsum(np.random.uniform(-0.001, 0.001, num_rows)),
}

df = pd.DataFrame(data)

# Sauvegarder le fichier CSV
csv_path = "C:/Users/Tom/Documents/ecole/INGE 3TD/projets/network_mon_dash/backend/app/data/Trace/faux_donnees_deplacement.csv"
df.to_csv(csv_path, index=False)

csv_path
