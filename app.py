from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 🔹 Configurar tu clave API de OpenAI
OPENAI_API_KEY = "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" # Reemplázala con tu clave real

# Configurar OpenAI API
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
            messages=[{"role": "system", "content": "Eres Atlas AI, una inteligencia avanzada que ayuda a Marco."},
                      {"role": "user", "content": user_message}]
        )

        atlas_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": atlas_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

