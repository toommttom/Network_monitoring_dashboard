import uvicorn
from app import app  # Import de l'application FastAPI

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=5000, reload=True)