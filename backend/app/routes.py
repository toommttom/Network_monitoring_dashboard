import os
import glob
import pandas as pd
import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

# 📂 Dossiers des fichiers CSV
FOLDER_PATH = "backend/app/data/Trace/"
FOLDER_PATH_SESSION = "backend/app/data/Session/"

#  Fonction pour normaliser les dates
def format_dates(df):
    column_rename = {"Moment du ping": "Moment_du_ping" ,
                     "throuput": "Throuput" }
    df.rename(columns=column_rename, inplace=True)

    date_columns = ["Date_Performance", "Moment_du_ping"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df

#  Route pour récupérer les données 
@router.get("/api/data")
async def get_all_data():
    csv_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

    if not csv_files:
        raise HTTPException(status_code=404, detail="Aucun fichier trouvé")

    all_data = []
    for file in csv_files:
        df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
        df = format_dates(df)
        df = df[["Moment_du_ping", "Latence", "server_name", "Technologie_Reseau", "Ville","Input","Output", "ID_user", "Throuput", "Jitter"]]  # Réduire la taille du JSON
        df["source_file"] = os.path.basename(file)  # Ajouter une colonne pour identifier la source
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.replace({np.nan: None})

    return JSONResponse(content=final_df.to_dict(orient="records"))

#  Route pour récupérer un fichier spécifique
@router.get("/api/data/{filename}")
async def get_specific_data(filename: str):
    file_path = os.path.join(FOLDER_PATH, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier {filename} introuvable")

    try:
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
        df = format_dates(df)

        if "server_name" not in df.columns:
            raise HTTPException(status_code=400, detail="Colonne 'server_name' manquante dans le fichier")

        expected_columns = ["Moment_du_ping", "Latence", "server_name", "Jitter", "Packetloss", "Throuput"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None


        df = df.replace({np.nan: None})

        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier: {str(e)}")

# 📌 Route pour obtenir la liste des fichiers
@router.get("/api/files")
async def get_files():
    csv_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

    if not csv_files:
        raise HTTPException(status_code=404, detail="Aucun fichier trouvé")

    file_list = [os.path.basename(file) for file in csv_files]
    return {"files": file_list}

# 📌 Route pour récupérer les événements (latence élevée, jitter, débit faible)
@router.get("/api/events")
async def get_events():
    csv_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

    if not csv_files:
        raise HTTPException(status_code=404, detail="Aucun fichier de données trouvé")

    events = []

    for file in csv_files:
        df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
        df = format_dates(df)

        # 🔥 Remplacement des valeurs NaN et infinies
        df.replace([np.nan, np.inf, -np.inf], None, inplace=True)
        df.dropna(subset=["Latence", "Jitter", "Throuput"], inplace=True)

        for _, row in df.iterrows():
            try:
                # Vérifier que les valeurs numériques sont bien des nombres
                latence = float(row.get("Latence", 0))
                jitter = float(row.get("Jitter", 0))
                throuput = float(row.get("Throuput", 0))

                if latence > 200:
                    events.append({
                        "type": "Latence élevée",
                        "description": f"Latence de {latence} ms détectée",
                        "timestamp": row.get("Date_Performance", "Inconnu"),
                        "file": os.path.basename(file)
                    })

                if jitter > 100:
                    events.append({
                        "type": "Jitter excessif",
                        "description": f"Jitter de {jitter} ms détecté",
                        "timestamp": row.get("Date_Performance", "Inconnu"),
                        "file": os.path.basename(file)
                    })

                if throuput < 500:
                    events.append({
                        "type": "Débit faible",
                        "description": f"Débit de {throuput} kbps détecté",
                        "timestamp": row.get("Date_Performance", "Inconnu"),
                        "file": os.path.basename(file)
                    })

            except ValueError:
                print(f"⚠️ Erreur de conversion dans {file} à la ligne {row}")
                continue  # Ignore la ligne problématique

    return JSONResponse(content=events)


# 📌 Route pour récupérer les statistiques globales
@router.get("/api/stats")
async def get_stats():
    csv_files = glob.glob(os.path.join(FOLDER_PATH, "*.csv"))

    if not csv_files:
        return {
            "totalTests": 0,
            "avgLatency": 0.0,
            "maxLatency": 0
        }

    all_data = []
    for file in csv_files:
        df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    if "Latence" not in final_df.columns:
        return {
            "totalTests": len(final_df),
            "avgLatency": 0.0,
            "maxLatency": 0
        }

    total_tests = len(final_df)
    avg_latency = final_df["Latence"].mean() if not final_df["Latence"].isna().all() else 0.0
    max_latency = final_df["Latence"].max() if not final_df["Latence"].isna().all() else 0

    return {
        "totalTests": total_tests,
        "avgLatency": round(avg_latency, 2),
        "maxLatency": max_latency
    }


@router.get("/api/clustering-plot")
async def get_clustering_plot():
    # Charger les données (même logique que ton script actuel)
    file_path = os.path.join(FOLDER_PATH, "data_tracesV2-P1.csv")
    df = pd.read_csv(file_path)
    df = df.dropna(subset=['Latence'])
    df.rename(columns={"Moment du ping": "Moment_du_ping", "throuput": "Throuput"}, inplace=True)
    df['Moment_du_ping'] = pd.to_datetime(df['Moment_du_ping'], errors='coerce')
    df = df.dropna(subset=['Moment_du_ping'])
    df['Heure'] = df['Moment_du_ping'].dt.hour
    df['Jour'] = df['Moment_du_ping'].dt.dayofweek
    df['Ville_Code'] = LabelEncoder().fit_transform(df['Ville'])

    features = ['Latence', 'Jitter', 'Heure', 'Jour', 'Ville_Code']
    X = df[features]
    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # 📊 Création du graphe
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df['Heure'], df['Latence'], c=df['Cluster'], cmap='viridis', alpha=0.6)
    plt.colorbar(scatter, label="Cluster")
    ax.set_xlabel("Heure de la journée")
    ax.set_ylabel("Latence (ms)")
    ax.set_title("Clusters de latence en fonction de l'heure")
    ax.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)

    return StreamingResponse(buffer, media_type="image/png")

@router.get("/api/random-forest-plot")
async def get_random_forest_plot():
    file_path = os.path.join(FOLDER_PATH, "data_tracesV2-P1.csv")
    df = pd.read_csv(file_path)

    df.rename(columns={"Moment du ping": "Moment_du_ping", "throuput": "Throuput"}, inplace=True)
    df['Moment_du_ping'] = pd.to_datetime(df['Moment_du_ping'], errors='coerce')
    df = df.dropna(subset=['Moment_du_ping'])
    df['Heure'] = df['Moment_du_ping'].dt.hour
    df['Jour'] = df['Moment_du_ping'].dt.dayofweek
    df['Ville_Code'] = LabelEncoder().fit_transform(df['Ville'])

    features = ['Jitter', 'Heure', 'Jour', 'Ville_Code', 'Throuput']
    target = 'Latence'
    df = df.dropna(subset=features + [target])

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    # 📊 Création du graphe
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(y_test, y_pred, alpha=0.5, color='blue')
    ax.plot(
        [min(y_test), max(y_test)],
        [min(y_test), max(y_test)],
        color='red',
        linestyle='dashed'
    )
    ax.set_xlabel("Valeurs réelles de Latence")
    ax.set_ylabel("Valeurs prédites de Latence")
    ax.set_title("Prédiction de la latence avec RandomForest")
    ax.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)

    return StreamingResponse(buffer, media_type="image/png")
