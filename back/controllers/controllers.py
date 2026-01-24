from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from models.dtos import DTOCoordinates, DTOCoordinatesPaginated
from interfaces import InterfaceController
from models.schemas import User, Keys, Geolocation, Coordinates, Order
from dbconfig.base import Base as SQLAlchemyBase
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class BusinessController(InterfaceController):        
    def validate_response(self, model: SQLAlchemyBase, DTO: BaseModel, 
                          log_message: str = "DTO validado c/ sucesso"):
        response = DTO.model_validate(model)
        logger.debug(log_message)
        return response
    



class UserController(BusinessController):        
    def validate_response(self, model: User, DTO: BaseModel, log_message: str = "User controller validou response c/ sucesso"):
        return super().validate_response(model=model, 
                                         DTO=DTO,
                                         log_message=log_message)




class GeolocationController(BusinessController):        
    def validate_response(self, model: Geolocation, DTO: BaseModel, log_message: str = "Geolocation controller validou response c/ sucesso"):
        return super().validate_response(model=model, 
                                         DTO=DTO,
                                         log_message=log_message)
    




class CoordinatesController(BusinessController):        
    #@staticmethod
    def validate_response(self, model: Coordinates, DTO: BaseModel, log_message: str = "Coordinates controller validou response c/ sucesso"):
        return super().validate_response(model=model, 
                                         DTO=DTO,
                                         log_message=log_message)
    
    @staticmethod
    def validate_response_paginated(model: dict):
        return DTOCoordinatesPaginated(
            items=[
                DTOCoordinates.model_validate(item)
                for item in model["items"]
            ],
            next_cursor=model["next_cursor"]
        )
    


class KeysController(BusinessController):        
    #@staticmethod
    def validate_response(self, model: Keys, DTO: BaseModel, log_message: str = "Geolocation controller validou response c/ sucesso"):
        return super().validate_response(model=model, 
                                         DTO=DTO,
                                         log_message=log_message)



class OrderController(BusinessController):        
    #@staticmethod
    def validate_response(self, model: Order, DTO: BaseModel, log_message: str = "Order controller validou response c/ sucesso"):
        return super().validate_response(model=model, 
                                         DTO=DTO,
                                         log_message=log_message)
    @staticmethod
    def validate_response_getorder(model: dict, log_message: str = "Order controller validou response c/ sucesso"):
        from models.dtos import DTOGetOrderResponse
        
        response = DTOGetOrderResponse.model_validate(model)
        logger.debug(log_message)
        return response