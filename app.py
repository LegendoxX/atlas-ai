from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos simple para almacenar mensajes temporalmente
messages = []

@app.route('/chat', methods=['POST'])
def chat():
    """Recibe un mensaje del usuario y responde."""
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No se recibió mensaje"}), 400

    # Aquí puedes personalizar la respuesta de Atlas AI
    response_message = f"Atlas: Recibí tu mensaje - '{user_message}'"

    # Guardamos el mensaje en la "base de datos" temporal
    messages.append({"user": user_message, "atlas": response_message})

    return jsonify({"response": response_message})

@app.route('/chat/history', methods=['GET'])
def chat_history():
    """Devuelve el historial de mensajes."""
    return jsonify({"messages": messages})

@app.route('/')
def home():
    return jsonify({"message": "Atlas AI está funcionando 🚀"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
