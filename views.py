import os
from flask import Flask, request, jsonify, Response, Blueprint
import tempfile
from transcribe_audio import transcribe_audio

audio = Blueprint('audio', __name__)

@audio.route('/audio', methods=['POST'])
def handle_audio():
    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        audio_file.save(temp_file.name)
    
    try:
        transcription = transcribe_audio(temp_file.name)
        if transcription is None:
            return jsonify({"error": "Transcription failed"}), 500
        return Response(transcription, mimetype='application/json'), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    finally:
        os.remove(temp_file.name)
