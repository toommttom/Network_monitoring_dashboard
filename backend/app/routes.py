import os
import glob
import pandas as pd
from flask import jsonify
from app import app
import numpy as np


#================= Fonction pour normaliser les dates
def format_dates(df):
    column_rename = {"Moment du ping" : "Moment_du_ping"}
    df.rename(columns=column_rename, inplace=True)


    date_columns = ["Date_Performance", "Moment_du_ping"]  # Colonnes à formater

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")  # Convertir en datetime, gérer erreurs
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")  # Uniformiser en YYYY-MM-DD HH:mm:ss

    return df

@app.route('/api/data', methods=['GET'])
def get_data():
    folder_path = "backend/app/data/Trace/"  # Dossier contenant les fichiers CSV
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Liste de tous les fichiers CSV
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier CSV trouvé"}), 404

    all_data = []  # Liste pour stocker les données

    for file in csv_files:
        df = pd.read_csv(file)  # Lire le CSV
        df["source_file"] = os.path.basename(file)  # Ajouter une colonne pour identifier la source
        df = format_dates(df)  #  Normaliser les dates
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)  # Fusionner tous les fichiers en un seul DataFrame
    final_df = final_df.replace({np.nan: None})

    return jsonify(final_df.to_dict(orient='records'))  # Convertir en JSON et retourner


@app.route('/api/data/<filename>', methods=['GET'])
def get_specific_data(filename):
    folder_path = "backend/app/data/Trace/"
    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": f"Fichier {filename} introuvable"}), 404

    df = pd.read_csv(file_path)
    df = format_dates(df)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/files', methods=['GET'])
def get_files():
    folder_path = "backend/app/data/Trace/"
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier trouvé"}), 404

    file_list = [os.path.basename(file) for file in csv_files]  # Liste des noms de fichiers
    return jsonify({"files": file_list})


@app.route('/api/events', methods=['GET'])
def get_events():
    folder_path = "backend/app/data/Trace/"  # Récupérer les fichiers de données
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier de données trouvé"}), 404

    events = []
    
    for file in csv_files:
        df = pd.read_csv(file)
        df = format_dates(df)
        
        for _, row in df.iterrows():
            if row.get("Latence", 0) > 200:
                events.append({
                    "type": "Latence élevée",
                    "description": f"Latence de {row['Latence']} ms détectée",
                    "timestamp": row.get("Date_Performance", "Inconnu"),
                    "file": os.path.basename(file)
                })
            
            if row.get("Jitter", 0) > 100:
                events.append({
                    "type": "Jitter excessif",
                    "description": f"Jitter de {row['Jitter']} ms détecté",
                    "timestamp": row.get("Date_Performance", "Inconnu"),
                    "file": os.path.basename(file)
                })
            
            if row.get("Throuput", 10000) < 500:
                events.append({
                    "type": "Débit faible",
                    "description": f"Débit de {row['Throuput']} kbps détecté",
                    "timestamp": row.get("Date_Performance", "Inconnu"),
                    "file": os.path.basename(file)
                })
    
    return jsonify(events)

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    folder_path = "backend/app/data/Session/"  # Dossier contenant les fichiers de sessions
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Liste de tous les fichiers CSV
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier de session trouvé"}), 404

    all_data = []  # Liste pour stocker les sessions

    for file in csv_files:
        df = pd.read_csv(file)  # Lire le CSV
        df["source_file"] = os.path.basename(file)  # Ajouter une colonne pour identifier la source
        df = format_dates(df)  # Normaliser les dates
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)  # Fusionner tous les fichiers en un seul DataFrame
    final_df = final_df.replace({np.nan: None})

    return jsonify(final_df.to_dict(orient='records'))  # Convertir en JSON et retourner

import os
import glob
import pandas as pd
import numpy as np
from flask import jsonify
from app import app

# ================= API pour récupérer les statistiques globales =================
@app.route('/api/stats', methods=['GET'])
def get_stats():
    folder_path = "backend/app/data/Trace/"  # Dossier contenant les fichiers CSV des traces
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Liste des fichiers CSV
    
    if not csv_files:
        return jsonify({
            "totalTests": 0,
            "avgLatency": 0.0,
            "maxLatency": 0
        })

    all_data = []  # Stocker toutes les données
    
    for file in csv_files:
        df = pd.read_csv(file)
        all_data.append(df)

    # Fusionner tous les fichiers CSV en un seul DataFrame
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Vérifier que la colonne "Latence" existe
    if "Latence" not in final_df.columns:
        return jsonify({
            "totalTests": len(final_df),
            "avgLatency": 0.0,
            "maxLatency": 0
        })

    # Calculer les statistiques
    total_tests = len(final_df)
    avg_latency = final_df["Latence"].mean() if not final_df["Latence"].isna().all() else 0.0
    max_latency = final_df["Latence"].max() if not final_df["Latence"].isna().all() else 0

    return jsonify({
        "totalTests": total_tests,
        "avgLatency": round(avg_latency, 2),
        "maxLatency": max_latency
    })


