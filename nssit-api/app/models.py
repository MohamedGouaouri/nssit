from flask_login import UserMixin
from time import time
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Padding import appendPadding, removePadding
from app import db
import base64


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(50), index=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50))
    password_enc = db.Column(db.String())

    def __init__(self, service, username, email, password, key):
        self.service = service
        self.username = username
        self.email = email
        self.password_enc = self.encrypt(password, key)

    def encrypt(self, password, key):
        aes = AES.new(key, AES.MODE_ECB)
        padded = appendPadding(password)
        return base64.b64encode(aes.encrypt(padded))

    def decrypt(self, key):
        aes = AES.new(key, AES.MODE_ECB)
        plain = aes.decrypt(base64.b64decode(self.password_enc))
        return removePadding(plain.decode())
