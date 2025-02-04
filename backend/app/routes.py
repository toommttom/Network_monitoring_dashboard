import os
import glob
import pandas as pd
from flask import jsonify
from app import app


#================= Fonction pour normaliser les dates
def format_dates(df):
    date_columns = ["Date_Performance", "Moment du ping"]  # Colonnes à formater

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
