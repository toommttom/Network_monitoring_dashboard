from flask import jsonify
import pandas as pd
from app import app

@app.route('/api/data', methods=['GET'])
def get_data():
    df = pd.read_csv('app/data/Trace/data.csv')
    data = df.to_dict(orient='records')
    return jsonify(data)
