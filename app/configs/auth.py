from flask_jwt_extended import JWTManager
from flask import Flask


def init_app(app: Flask):
    JWTManager(app)
