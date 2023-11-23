#!/usr/bin/python3
"""
Simple REST API Module
"""
from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from os import getenv
from views import audio,cleanup_extracted_data

def create_app():
    load_dotenv()
    app = Flask(__name__)
    scheduler = APScheduler()
    scheduler.init_app(app)
    app.scheduler = scheduler
    
    scheduler.add_job(id='Scheduled Cleanup', func=cleanup_extracted_data,
                      trigger='interval', seconds=3600)
    
    scheduler.start()
    
    app.register_blueprint(audio)
    return app

if __name__ == '__main__':
    app = create_app()
    
    API_HOST = getenv('API_HOST')
    API_PORT = getenv('API_PORT')

    host = API_HOST if API_HOST else '0.0.0.0'
    port = API_PORT if API_PORT else 5000

    app.run(port=port, host=host, debug=True)
