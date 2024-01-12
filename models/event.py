#!/usr/bin/env python3
"""
Event Collection
"""

from mongoengine import *

class Event(Document):
    meta = {"collection": "events"}
    summary = StringField(max_length=255, required=True)
    description = StringField(max_length=1024, required=True)
    start = DateField()
    end = DateField()
    google_Id = StringField(max_length=255, required=True)
