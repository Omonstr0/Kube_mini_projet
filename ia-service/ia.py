from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get("text", "")
    prediction = f"Je prédis : {text[::-1]}"  # renvoie le texte inversé pour simuler une IA
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
