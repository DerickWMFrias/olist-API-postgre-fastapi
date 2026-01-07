from fastapi import FastAPI
from errors import register_exceptions
from routes import register_routes
from app_factory import create_app

app = create_app()