from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .test import router as test_router
from .users import router as user_router
from .geolocation import router as geo_router

def register_routes(app: FastAPI):
    app.include_router(test_router)
    app.include_router(user_router)
    app.include_router(geo_router)
    
