from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permet la communication avec le frontend

from app import routes
