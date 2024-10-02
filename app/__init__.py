from flask import Flask
from app.routes import create_routes

def create_app():
    app = Flask(__name__)
    create_routes(app)
    return app
