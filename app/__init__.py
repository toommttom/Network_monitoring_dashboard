from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import router  # Import des routes FastAPI

# Création de l'application FastAPI
app = FastAPI()

# Autoriser les requêtes du frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (à sécuriser en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes définies dans routes.py
app.include_router(router)
