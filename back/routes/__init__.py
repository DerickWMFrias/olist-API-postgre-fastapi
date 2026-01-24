from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .hello import router as hello_router
from .users import router as user_router
from .geolocation import router as geo_router
from .keys import router as keys_router
from .orders import router as order_router

def register_routes(app: FastAPI):
    app.include_router(hello_router)
    app.include_router(user_router)
    app.include_router(geo_router)
    app.include_router(keys_router)
    app.include_router(order_router)
    
