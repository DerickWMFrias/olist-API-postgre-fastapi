from abc import ABC, abstractmethod
from pydantic import BaseModel
from fastapi import Request
from dbconfig.base import Base
from typing import Dict

"""
Interface implementada por controladores que validam algum DTO
"""
class InterfaceController(ABC):
    @abstractmethod
    async def validate_response(self, model: Base, DTO: BaseModel):
        """Este método DEVE ser implementado pelas subclasses"""
        pass




class InterfaceService(ABC):
    @abstractmethod
    async def get_data(self, payload: Dict):
        pass


    @abstractmethod
    async def register(self, payload: BaseModel):
        pass


    @abstractmethod
    async def patch(self, payload: BaseModel):
        pass


    @abstractmethod
    async def delete(self, payload: BaseModel):
        pass