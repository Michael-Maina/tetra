from math import e
import os
import time
import threading
from flask import Flask, request, jsonify, Response, Blueprint
import tempfile
from transcribe_audio import transcribe_audio
from extract_entities import extract_entities

audio = Blueprint('audio', __name__)

extracted_data_storage = {}

@audio.route('/audios', methods=['POST'])
def handle_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "File not found"}), 404
    
    temp_file = None
    try:
        audio_file = request.files['audio']
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            audio_file.save(temp_file.name)

        transcription_text = transcribe_audio(temp_file.name)
        
        if transcription_text is None:
            return jsonify({"error": "Transcription failed"}), 500
        
        extracted_data = extract_entities(transcription_text)
        
        data_key = str(hash(transcription_text))
        current_time = time.time()
        
        extracted_data_storage[data_key] = {
            "extracted_data":extracted_data,
            "timestamp": current_time
            }
        
        return jsonify({
            "transcription_text": transcription_text,
            "data_key": data_key, 
        })
    finally:
        if temp_file and os.path.exists(temp_file.name):
            os.remove(temp_file.name)

@audio.route('/extracted_data/<data_key>', methods=['GET'])
def get_extracted_data(data_key):
    if data_key in extracted_data_storage:
        return (extracted_data_storage[data_key]["extracted_data"]), 200
    else:
        return jsonify({"error": "Data not found"}), 404

def cleanup_extracted_data():
    expiration_threshold = 3600
    current_time = time.time()
    keys_to_delete = [key for key, value in extracted_data_storage.items()
                      if current_time - value["timestamp"] > expiration_threshold]
    for key in keys_to_delete:
        del extracted_data_storage[key]
