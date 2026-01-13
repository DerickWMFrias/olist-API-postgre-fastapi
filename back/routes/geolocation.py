import logging
from dbconfig.conn import get_dbconn
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.dtos import DTOUserRegister
from controllers.controllers import GeolocationController, CoordinatesController
from services.geolocation import CoordinatesService, GeolocationService
from sqlalchemy.orm import Session
from uuid import UUID
from errors.errors import NotFoundError, ConflictError, UnauthorizedError, BadRequestError
from models.dtos import DTOGeolocation, DTOCoordinates
from pydantic import EmailStr
from lib.api_validation import validate_api_key


router = APIRouter(prefix="/geo",
                   tags=["Geolocation"],
                   responses={},
                   dependencies=[Depends(validate_api_key)])


@router.get("/", status_code=status.HTTP_200_OK)
def geolocation_get_geolocation(
    dbconn: Session = Depends(get_dbconn),
    zipcode_prefix: str = Query(..., max_length=8, description=""),
):
    try:
        service = GeolocationService(dbconn)
        controller = GeolocationController()

        new_user = service.get_data(payload=dict(geolocation_zip_code_prefix=zipcode_prefix))
        response = controller.validate_response(model=new_user,
                                                DTO=DTOGeolocation)
        return response
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting geolocation"
        )



@router.get("/coordinate", status_code=status.HTTP_200_OK)
def coordinates_get_coordinate(
    dbconn: Session = Depends(get_dbconn),
    coordinate_id: UUID = Query(..., description=""),
):
    try:
        service = CoordinatesService(dbconn)
        controller = CoordinatesController()

        new_user = service.get_data(payload=dict(coordinate_id=coordinate_id))
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


@router.get("/coordinates", status_code=status.HTTP_200_OK)
def coordinates_get_coordinate(
    dbconn: Session = Depends(get_dbconn),
    limit: int = Query(20, le=50, ge=1, description=""),
    cursor: str = Query(None, description="")
):
    try:
        service = CoordinatesService(dbconn)
        controller = CoordinatesController()

        data_dict = service.get_data_paginated(payload=dict(limit=limit, 
                                                 cursor=cursor,
                                                 zipcode_prefix=None))
        response = controller.validate_response_paginated(model=data_dict)
        return response
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering coordinate"
        )



@router.get("/coordinates/{zipcode_prefix}", status_code=status.HTTP_200_OK)
def coordinates_get_coordinate(
    zipcode_prefix: str,
    dbconn: Session = Depends(get_dbconn),
    limit: int = Query(20, le=50, ge=1, description=""),
    cursor: str = Query(None, description="")
):
    try:
        service = CoordinatesService(dbconn)
        controller = CoordinatesController()

        data_dict = service.get_data_paginated(payload=dict(limit=limit, 
                                                 cursor=cursor,
                                                 zipcode_prefix=zipcode_prefix))
        response = controller.validate_response_paginated(model=data_dict)
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


@router.post("/coordinate", status_code=status.HTTP_201_CREATED)
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
    except BadRequestError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering coordinate"
        )
    



@router.delete("/{geolocation_zip_code_prefix}", status_code=status.HTTP_204_NO_CONTENT)
def geolocation_post_geolocation(
    geolocation_zip_code_prefix: str,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = GeolocationService(dbconn)

        service.delete(dict(geolocation_zip_code_prefix=geolocation_zip_code_prefix))
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering geolocation"
        )

    return None

@router.delete("/coordinate/{coordinate_id}", status_code=status.HTTP_204_NO_CONTENT)
def coordinates_post_coordinate(
    coordinate_id: UUID,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = CoordinatesService(dbconn)
        service.delete(dict(coordinate_id=coordinate_id))
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering coordinate"
        )
    
    return None