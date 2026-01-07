from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from models.dtos import DTOUserRegister, DTOUserResponse
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