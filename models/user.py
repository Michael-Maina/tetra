#!/usr/bin/python3
"""
User Collection
"""
from flask_login import UserMixin
from mongoengine import *


class User(UserMixin, Document):
    meta = {'collection': 'users'}
    email = EmailField(allow_utf8_user=False, allow_ip_domain=False, required=True)
    first_name = StringField(max_length=255, required=True)
    last_name = StringField(max_length=255, required=True)
    refresh_token = StringField(max_length=255, required=True)

    def __repr__(self):
        return f'User: {str(self.email)}'

    def get_id(self):
        return str(self.id)
