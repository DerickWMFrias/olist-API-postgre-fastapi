import logging
from dbconfig.conn import get_dbconn
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.dtos import DTOUserRegister
from controllers.controllers import GeolocationController, CoordinatesController
from services.geolocation import CoordinatesService, GeolocationService
from sqlalchemy.orm import Session
from uuid import UUID
from errors.errors import NotFoundError, ConflictError, UnauthorizedError
from models.dtos import DTOGeolocation, DTOCoordinates
from pydantic import EmailStr



router = APIRouter(prefix="/geo",
                   tags=["Geolocation"],
                   responses={},
                   dependencies=[])


@router.get("/", status_code=status.HTTP_200_OK)
def geolocation_get_geolocation(
    dbconn: Session = Depends(get_dbconn),
    zipcode_prefix: str = Query(..., max_length=8, description=""),
):
    try:
        service = GeolocationService(dbconn)
        controller = GeolocationController()

        new_user = service.get_data(payload=dict(zipcode=zipcode_prefix))
        response = controller.validate_response(model=new_user,
                                                DTO=DTOGeolocation)
        return response
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering geolocation"
        )


@router.get("/coordinates", status_code=status.HTTP_200_OK)
def coordinates_get_coordinate(
    dbconn: Session = Depends(get_dbconn),
    zipcode_prefix: str = Query(..., max_length=8, description=""),
):
    try:
        service = CoordinatesService(dbconn)
        controller = CoordinatesController()

        new_user = service.get_data(payload=dict(zipcode=zipcode_prefix))
        response = controller.validate_response(model=new_user,
                                                DTO=DTOCoordinates)
        return response
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering coordinate"
        )





@router.post("/", status_code=status.HTTP_201_CREATED)
def geolocation_post_geolocation(
    payload: DTOGeolocation,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = GeolocationService(dbconn)
        controller = GeolocationController()

        new_user = service.register(payload=payload)
        response = controller.validate_response(model=new_user,
                                                DTO=DTOGeolocation)
        return response
    except ConflictError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering geolocation"
        )


@router.post("/coordinates", status_code=status.HTTP_201_CREATED)
def coordinates_post_coordinate(
    payload: DTOCoordinates,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = CoordinatesService(dbconn)
        controller = CoordinatesController()

        new_user = service.register(payload=payload)
        response = controller.validate_response(model=new_user,
                                                DTO=DTOCoordinates)
        return response
    except ConflictError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering coordinate"
        )