from flask import Flask, request, jsonify
from gtts import gTTS
import os
import speech_recognition as sr  # Para reconocimiento de voz

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    """Convierte texto en voz y devuelve el audio."""
    data = request.json
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No se recibió texto"}), 400

    # Generar el audio con gTTS
    tts = gTTS(text=text, lang="es")
    tts.save("response.mp3")

    return jsonify({"message": "Audio generado con éxito", "file": "response.mp3"})

@app.route('/voice-command', methods=['POST'])
def voice_command():
    """Reconoce un comando de voz y lo devuelve como texto."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio, language="es-ES")
        return jsonify({"response": command})
    except sr.UnknownValueError:
        return jsonify({"error": "No se pudo reconocer el comando"}), 400

@app.route('/')
def home():
    return jsonify({"message": "Atlas AI está funcionando 🚀"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
