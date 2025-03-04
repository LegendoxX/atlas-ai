import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# 🔹 Configurar tu clave API de OpenAI desde variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Falta la clave API de OpenAI. Configúrala como variable de entorno.")

openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Atlas AI está funcionando 🚀"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No se recibió ningún mensaje"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres Atlas AI, una inteligencia avanzada que ayuda a Marco."},
                {"role": "user", "content": user_message}
            ]
        )

        atlas_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": atlas_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

