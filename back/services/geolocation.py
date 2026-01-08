import os
import bcrypt
import logging
from uuid import uuid4
from models.dtos import DTOGeolocation, DTOCoordinates
from models.schemas import Geolocation, Coordinates
from errors.errors import ConflictError, NotFoundError, UnauthorizedError
from uuid import UUID
from fastapi import HTTPException
from pydantic import EmailStr
from interfaces import InterfaceService
from typing import Dict


logger = logging.getLogger(__name__)


class GeolocationService(InterfaceService):
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.dbconn = db

    def get_data(self, payload: Dict):
        data = self.dbconn.query(Geolocation).filter(Geolocation.geolocation_zip_code_prefix == payload["zipcode"]).first()
        if not data:
            raise NotFoundError(
                err_msg="Could not find such geolocation.",
                log_msg=f"Geolocation w/ zipcode {payload["zipcode"]} not found"
            )

        return data
    
    def register(self, payload: DTOGeolocation):
        geolocation_exists = self.dbconn.query(Geolocation).filter(Geolocation.geolocation_zip_code_prefix == payload.geolocation_zip_code_prefix).first()
        if geolocation_exists:
            raise ConflictError 

        # 3. SALVA NO BANCO
        new_geolocation = Geolocation(
            geolocation_zip_code_prefix=payload.geolocation_zip_code_prefix,
            geolocation_city=payload.geolocation_city,
            geolocation_state=payload.geolocation_state
        )

        # 4. ADD NO BANCO
        self.dbconn.add(new_geolocation)
        self.dbconn.commit()
        self.dbconn.refresh(new_geolocation)

        logging.debug(f"Successful register of geolocation w/ zipcode: {payload.geolocation_zip_code_prefix}")
        return new_geolocation
    
    def patch(self, payload: DTOGeolocation):
        return super().patch(payload)
    
    def delete(self, payload: DTOGeolocation):
        return super().delete(payload)


class CoordinatesService(InterfaceService):
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.dbconn = db


    def get_data(self, payload: Dict):
        data = self.dbconn.query(Coordinates).filter(Coordinates.geolocation_zip_code_prefix == payload["zipcode"]).first()
        if not data:
            raise NotFoundError(
                err_msg="Could not find such coordinates.",
                log_msg=f"Coordinates w/ zipcode {payload['zipcode']} not found"
            )

        return data
    
    def register(self, payload):
        coordinate_exists = self.dbconn.query(Coordinates).filter(Coordinates.geolocation_zip_code_prefix == payload.geolocation_zip_code_prefix).first()
        if coordinate_exists:
            raise ConflictError 

        new_coordinate = Coordinates(
            geolocation_zip_code_prefix=payload.geolocation_zip_code_prefix,
            lat=payload.lat,
            lng=payload.lng
        )
        
        self.dbconn.add(new_coordinate)
        self.dbconn.commit()
        self.dbconn.refresh(new_coordinate)

        logging.debug(f"Successful register of coordinate w/ lat: {payload.lat} lng: {payload.lng}")
        return new_coordinate
    
    
    def patch(self, payload):
        return super().patch(payload)
    
    def delete(self, payload):
        return super().delete(payload)