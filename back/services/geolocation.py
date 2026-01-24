import logging
from models.dtos import DTOGeolocation
from errors.errors import ConflictError, NotFoundError, BadRequestError
from pydantic import BaseModel
from interfaces import InterfaceService
from typing import Dict
from repositories.geolocation import GeolocationRepository
from repositories.coordinates import CoordinatesRepository

logger = logging.getLogger(__name__)


class GeolocationService(InterfaceService):
    def __init__(self, db):
        self.dbconn = db
        self.repository = GeolocationRepository(db)

    def get_data(self, payload: Dict | DTOGeolocation):
        try:
            data = self.repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=payload["geolocation_zip_code_prefix"])

            if not data:
                raise NotFoundError(
                    err_msg="Could not find such geolocation.",
                    log_msg=f"Geolocation w/ zipcode {payload['geolocation_zip_code_prefix']} not found"
                )
        except Exception as e:
            raise e

        return data
    
    def register(self, payload:  Dict | DTOGeolocation):
        try:
            geolocation_exists = self.repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=payload.geolocation_zip_code_prefix)
            
            if geolocation_exists:
                raise ConflictError 

            new_geolocation = self.repository.add_geolocation(new_geolocation=payload)
            logging.debug(f"Successful register of geolocation w/ zipcode: {payload.geolocation_zip_code_prefix}")
        except Exception as e:
            raise e
        
        return new_geolocation
    
    def patch(self, payload:  Dict | DTOGeolocation):
        return super().patch(payload)
    

    def delete(self, payload:  Dict | DTOGeolocation):
        try:
            rows_deleted = self.repository.delete_geolocation(zipcode_prefix=payload["geolocation_zip_code_prefix"])

            if not rows_deleted:
                raise NotFoundError(err_msg="No geolocation w/ prefix.",
                                    log_msg="No geolocation w/ prefix.")
        except Exception as e:
            raise e


class CoordinatesService(InterfaceService):
    def __init__(self, db):
        self.dbconn = db
        self.repository = CoordinatesRepository(db=db)


    def get_data(self, payload:  Dict | BaseModel):
        try:
            data = self.repository.get_coordinates_data_by_coordinate_id(coordinate_id=payload["coordinate_id"])
            if not data:
                raise NotFoundError(
                    err_msg="Could not find such coordinates.",
                    log_msg=f"Coordinates w/ id {payload['coordinate_id']} not found"
                )
        except Exception as e:
            raise e

        return data
    
    def get_data_paginated(self, payload: Dict | BaseModel):
        try:
            limit = payload["limit"]
            cursor = payload.get("cursor")
            zipcode_prefix = payload["zipcode_prefix"]
            
            items, next_cursor = self.repository.get_paginated_coordinates(limit=limit, 
                                                                        cursor=cursor,
                                                                        zipcode_prefix=zipcode_prefix)
        except Exception as e:
            raise e

        return {
            "items": items,
            "next_cursor": next_cursor
        }

    def register(self, payload:  Dict | BaseModel):
        try:
            new_coordinate = self.repository.add_coordinate(new_coordinate=payload)

            logging.debug(f"Successful register of coordinate w/ lat: {payload.lat} lng: {payload.lng}")

            if not new_coordinate:
                raise BadRequestError
        except Exception as e: 
            raise e
        
        return new_coordinate
    
    
    def patch(self, payload: Dict | BaseModel):
        return super().patch(payload)
    
    def delete(self, payload: Dict | BaseModel):
        try:
            rows_deleted = self.repository.delete_coordinate(coordinate_id=payload["coordinate_id"])
            
            if not rows_deleted:
                raise NotFoundError(err_msg="User not found.",
                                    log_msg="User not found.")
        except Exception as e:
            raise e