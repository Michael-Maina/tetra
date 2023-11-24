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
    MAX_FILE_SIZE = 5 * 1024 * 1024
    if 'audio' not in request.files:
        return jsonify({"error": "File not found"}), 404
    
    temp_file = None
    try:
        audio_file = request.files['audio']
        audio_file.save('test_audio.mp3')
        transcription_text = transcribe_audio('./test_audio.mp3')
        
        if not allowed_file(audio_file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        if not is_file_size_allowed(audio_file, MAX_FILE_SIZE):
            return jsonify({"error": "File size exceeds limit"}), 413
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            audio_file.save(temp_file.name)

       # transcription_text = transcribe_audio(temp_file.name)
        
        if transcription_text is None:
            return jsonify({"error": "Transcription failed"}), 500
        
        extracted_data = extract_entities(transcription_text)

        print()
        print(transcription_text)
        print(extracted_data)
        print()
        
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
        if temp_file:
            temp_file.close()
        if temp_file and os.path.exists(temp_file.name):
            os.remove(temp_file.name)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_file_size_allowed(file, max_size):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    return file_size <= max_size

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
