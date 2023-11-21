#!/usr/bin/python3
"""
Simple REST API Module
"""
from dotenv import load_dotenv
from flask import Flask
from os import getenv
from views import audio

load_dotenv()
app = Flask(__name__)

app.register_blueprint(audio)

if __name__ == '__main__':
    API_HOST = getenv('API_HOST')
    API_PORT = getenv('API_PORT')

    host = API_HOST if API_HOST else '0.0.0.0'
    port = API_PORT if API_PORT else 5000

    app.run(port=port, host=host, debug=True)
