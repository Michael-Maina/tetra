import os
import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY_WHISPER")

def transcribe_audio(file_path):
    client = OpenAI()
    with open(file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
        )
    return transcript["text"] if "text" in transcript else None
