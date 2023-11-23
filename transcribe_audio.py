import os
import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path):
    client = OpenAI()
    try:
        with open(file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format='json'
            )
        return extract_transcription(str(transcript))

    except FileNotFoundError:
        return None

def extract_transcription(input_string):
    # Identify the start of the transcribed text
    start_index = input_string.find('Transcription(text="') + len('Transcription(text="')
    
    # Identify the end of the transcribed text
    end_index = input_string.rfind('")')
    
    # Extract and return the transcribed text
    return input_string[start_index:end_index]