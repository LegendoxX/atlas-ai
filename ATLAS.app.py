from flask import Flask, request, jsonify, render_template
import pyttsx3  # Para convertir texto en voz
import speech_recognition as sr  # Para reconocimiento de voz
import threading
import time

app = Flask(__name__)

# Configuración del logo de la aplicación
APP_LOGO = "static/Atlas.webp"  # Ruta del logo

# Base de datos simulada para la interacción
data_store = {"users": {}, "sessions": {}, "thoughts": []}

# Configurar el motor de texto a voz
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def background_thinking():
    """Proceso en segundo plano para generar pensamientos y enviarlos automáticamente."""
    while True:
        if data_store["thoughts"]:
            thought = data_store["thoughts"].pop(0)
            print(f"ATLAS pensando: {thought}")
            speak(thought)
        time.sleep(10)  # Controla la frecuencia con la que ATLAS genera pensamientos

# Iniciar el proceso de pensamiento automático
thinking_thread = threading.Thread(target=background_thinking, daemon=True)
thinking_thread.start()

@app.route('/')
def home():
    return render_template("index.html", logo=APP_LOGO)

@app.route('/connect', methods=['POST'])
def connect():
    user_id = request.json.get("user_id")
    if user_id not in data_store["users"]:
        data_store["users"][user_id] = {"name": f"User-{user_id}", "settings": {}}
    return jsonify({"message": "Conexión establecida", "user": data_store["users"][user_id]})

@app.route('/update', methods=['POST'])
def update():
    user_id = request.json.get("user_id")
    settings = request.json.get("settings", {})
    if user_id in data_store["users"]:
        data_store["users"][user_id]["settings"].update(settings)
        return jsonify({"message": "Configuración actualizada", "settings": data_store["users"][user_id]["settings"]})
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/message', methods=['POST'])
def message():
    user_id = request.json.get("user_id")
    message = request.json.get("message")
    response = f"ATLAS: Recibido '{message}' de {user_id}. Procesando..."
    speak(response)  # ATLAS responde en voz
    return jsonify({"response": response})

@app.route('/voice-command', methods=['POST'])
def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="es-ES")
        response = f"Comando recibido: {command}"
        speak(response)
        return jsonify({"response": response})
    except sr.UnknownValueError:
        return jsonify({"error": "No se pudo reconocer el comando"})

@app.route('/thoughts', methods=['POST'])
def add_thought():
    """Añadir un pensamiento para que ATLAS lo procese automáticamente."""
    thought = request.json.get("thought")
    data_store["thoughts"].append(thought)
    return jsonify({"message": "Pensamiento añadido", "thought": thought})

@app.route('/get-logo', methods=['GET'])
def get_logo():
    """Devuelve la ruta del logo de la aplicación."""
    return jsonify({"logo": APP_LOGO})

if __name__ == '__main__':
    app.run(debug=True)
