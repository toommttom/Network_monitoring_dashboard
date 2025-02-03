import os
import glob
import pandas as pd
from flask import jsonify
from app import app

@app.route('/api/data', methods=['GET'])
def get_data():
    # folder_path = os.path.abspath("backend/app/data/Trace")
    folder_path = "backend/app/data/Trace/"  # Dossier contenant les fichiers CSV
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))  # Liste de tous les fichiers CSV
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier CSV trouvé"}), 404

    all_data = []  # Liste pour stocker les données

    for file in csv_files:
        df = pd.read_csv(file)  # Lire le CSV
        df["source_file"] = os.path.basename(file)  # Ajouter une colonne pour identifier la source
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
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/files', methods=['GET'])
def get_files():
    folder_path = "backend/app/data/Trace/"
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        return jsonify({"error": "Aucun fichier trouvé"}), 404

    file_list = [os.path.basename(file) for file in csv_files]  # Liste des noms de fichiers
    return jsonify({"files": file_list})
