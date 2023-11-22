#!/usr/bin/python3
"""
Database Storage Class
"""
from dotenv import load_dotenv
from mongoengine import connect
from os import getenv

# Load environment variables
load_dotenv()

class DBStorage:
    """
    Establishes and manages connection to database
    """
    def __init__(self):
        DB_URI = getenv('MONGO_URI')
        connect(host=DB_URI)
