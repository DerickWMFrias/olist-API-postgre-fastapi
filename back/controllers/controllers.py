from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from models.dtos import DTOCoordinates, DTOCoordinatesPaginated
from interfaces import InterfaceController
from models.schemas import User
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class UserController(InterfaceController):        
    @staticmethod
    def validate_response(model: User, DTO: BaseModel):
        response = DTO.model_validate(model)
        logger.debug("User controller validou response c/ sucesso")
        return response
    



class GeolocationController(InterfaceController):        
    @staticmethod
    def validate_response(model: User, DTO: BaseModel):
        response = DTO.model_validate(model)
        logger.debug("Geolocation controller validou response c/ sucesso")
        return response
    




class CoordinatesController(InterfaceController):        
    @staticmethod
    def validate_response(model: User, DTO: BaseModel):
        response = DTO.model_validate(model)
        logger.debug("Coordinates controller validou response c/ sucesso")
        return response
    
    @staticmethod
    def validate_response_paginated(model: dict):
        return DTOCoordinatesPaginated(
            items=[
                DTOCoordinates.model_validate(item)
                for item in model["items"]
            ],
            next_cursor=model["next_cursor"]
        )