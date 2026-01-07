from fastapi import FastAPI
from errors import register_exceptions
from routes import register_routes
import logging
import sys
import os



def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,  # MUITO IMPORTANTE
    )



def create_app() -> FastAPI:
    setup_logging(os.getenv("LOG_LEVEL", "DEBUG"))

    app = FastAPI()

    register_exceptions(app)
    register_routes(app)
    return app
