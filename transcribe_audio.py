import openai
from openai import OpenAI

def transcribe_audio(file_path):
    client = OpenAI()
    with open(file_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
        )
    return transcript
