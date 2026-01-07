"""
Neste pacote, registramos no ouvinte global do FastAPI os erros customizados da .errors.py

Ao estourar um desses erros, ele sobe até o framework, que então retorna uma response apropriada
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .errors import (
    NotFoundError,
    NoEmailFoundError,
    EmailAlreadyRegisteredError,
    UnauthorizedError
)

logger = logging.getLogger(__name__)


def register_exceptions(app: FastAPI):
    
    @app.exception_handler(UnauthorizedError)
    async def not_found_handler(request: Request, exc: UnauthorizedError):
        logger.error(exc.log_msg or "Unauthorized")

        return JSONResponse(
            status_code=401,
            content={"message": exc.err_msg}
        )
    
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        logger.error(exc.log_msg or "Not Found")

        return JSONResponse(
            status_code=404,
            content={"message": exc.err_msg}
        )

    @app.exception_handler(NoEmailFoundError)
    async def email_not_found_handler(request: Request, exc: NoEmailFoundError):
        return JSONResponse(
            status_code=404,
            content={"message": exc.message}
        )
    
    @app.exception_handler(EmailAlreadyRegisteredError)
    async def email_already_registered_handler(request: Request, exc: EmailAlreadyRegisteredError):
        return JSONResponse(
            status_code=500,
            content={"message": exc.message}
        )