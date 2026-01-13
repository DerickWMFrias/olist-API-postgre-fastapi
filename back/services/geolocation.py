import os
import bcrypt
import logging
import uuid
from models.dtos import DTOGeolocation, DTOCoordinates
from models.schemas import Geolocation, Coordinates
from errors.errors import ConflictError, NotFoundError, UnauthorizedError, BadRequestError
from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from interfaces import InterfaceService
from typing import Dict


logger = logging.getLogger(__name__)


class GeolocationService(InterfaceService):
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.dbconn = db

    def get_data(self, payload: Dict | DTOGeolocation):
        data = self.dbconn.query(Geolocation).filter(Geolocation.geolocation_zip_code_prefix == payload["zipcode"]).first()
        if not data:
            raise NotFoundError(
                err_msg="Could not find such geolocation.",
                log_msg=f"Geolocation w/ zipcode {payload["zipcode"]} not found"
            )

        return data
    
    def register(self, payload:  Dict | DTOGeolocation):
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
    
    def patch(self, payload:  Dict | DTOGeolocation):
        return super().patch(payload)
    
    def delete(self, payload:  Dict | DTOGeolocation):
        rows_deleted = (
            self.dbconn
            .query(Geolocation)
            .filter(Geolocation.geolocation_zip_code_prefix == payload["geolocation_zip_code_prefix"])
            .delete(synchronize_session=False)
        )

        if not rows_deleted:
            raise NotFoundError(err_msg="No geolocation w/ prefix.",
                                log_msg="No geolocation w/ prefix.")
        
        self.dbconn.commit()


class CoordinatesService(InterfaceService):
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.dbconn = db


    def get_data(self, payload:  Dict | BaseModel):
        data = self.dbconn.query(Coordinates).filter(Coordinates.coordinate_id == payload["coordinate_id"]).first()
        if not data:
            raise NotFoundError(
                err_msg="Could not find such coordinates.",
                log_msg=f"Coordinates w/ id {payload['coordinate_id']} not found"
            )

        return data
    
    def get_data_paginated(self, payload: Dict | BaseModel):
        limit = payload["limit"]
        cursor = payload.get("cursor")
        zipcode_prefix = payload["zipcode_prefix"]
        
        query = None
        if not zipcode_prefix:
            query = (
                self.dbconn
                .query(Coordinates)
                .order_by(Coordinates.coordinate_id)
            )
        else:
            query = (
                self.dbconn
                .query(Coordinates)
                .filter(Coordinates.geolocation_zip_code_prefix == zipcode_prefix)
                .order_by(Coordinates.coordinate_id)
            )

        # Filtra por cursor
        if cursor:
            try:
                cursor_uuid = uuid.UUID(cursor)
            except BadRequestError:
                raise BadRequestError(err_msg="Cant process sent cursor",
                                      log_msg="Cant process sent cursor")

            query = query.filter(
                Coordinates.coordinate_id > cursor_uuid
            )

        results = query.limit(limit + 1).all()


        # Filtra se ha resultados p/ busca
        if not results:
            raise NotFoundError(
                err_msg="No coordinates found",
                log_msg="Empty pagination result"
            )


        # Gera proximo cursor
        has_next = len(results) > limit
        items = results[:limit]

        next_cursor = None
        if has_next:
            last = items[-1]
            next_cursor = str(last.coordinate_id)


        return {
            "items": items,
            "next_cursor": next_cursor
        }

    def register(self, payload:  Dict | BaseModel):
        #coordinate_exists = self.dbconn.query(Coordinates).filter(Coordinates.geolocation_zip_code_prefix == payload.geolocation_zip_code_prefix).first()
        #if coordinate_exists:
        #    raise ConflictError 
        try:
            new_coordinate = Coordinates(
                coordinate_id=uuid.uuid4(),
                geolocation_zip_code_prefix=payload.geolocation_zip_code_prefix,
                lat=payload.lat,
                lng=payload.lng
            )
            
            self.dbconn.add(new_coordinate)
            self.dbconn.commit()
            self.dbconn.refresh(new_coordinate)

            logging.debug(f"Successful register of coordinate w/ lat: {payload.lat} lng: {payload.lng}")
            return new_coordinate
        except: 
            raise BadRequestError
    
    
    def patch(self, payload: Dict | BaseModel):
        return super().patch(payload)
    
    def delete(self, payload: Dict | BaseModel):
        rows_deleted = (
            self.dbconn
            .query(Coordinates)
            .filter(Coordinates.coordinate_id == payload["coordinate_id"])
            .delete(synchronize_session=False)
        )

        if not rows_deleted:
            raise NotFoundError(err_msg="User not found.",
                                log_msg="User not found.")
        
        self.dbconn.commit()