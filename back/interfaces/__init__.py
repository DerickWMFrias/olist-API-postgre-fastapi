from abc import ABC, abstractmethod
from pydantic import BaseModel
from fastapi import Request
from dbconfig.base import Base

"""
Interface implementada por controladores que validam algum DTO
"""
class InterfaceController(ABC):
    @abstractmethod
    async def validate_response(self, model: Base, DTO: BaseModel):
        """Este método DEVE ser implementado pelas subclasses"""
        pass