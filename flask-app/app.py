from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = "mongodb://mongo-db:27017/"
client = MongoClient(MONGO_URI)
db = client["prediction_db"]
collection = db["predictions"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        # Appel au microservice IA
        response = requests.post('http://ia-service:5000/predict', json={"text": text})
        prediction = response.json().get("prediction", "Erreur")

        # Enregistrement en DB
        collection.insert_one({"input": text, "prediction": prediction})

        return f"Texte : {text}<br>Prédiction : {prediction}"

    return '''
        <h1>Mini Prédiction</h1>
        <form method="POST">
            <input name="text" placeholder="Tape un mot" required>
            <button type="submit">Envoyer</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
