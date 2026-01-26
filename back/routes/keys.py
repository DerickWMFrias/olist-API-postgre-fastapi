import logging
from dbconfig.conn import get_dbconn
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.dtos import DTOUserRegister
from controllers.controllers import KeysController
from services.keys import KeysService
from sqlalchemy.orm import Session
from uuid import UUID
from errors.errors import BusinessError
from models.dtos import DTOUserAndPassword, DTONewKeygenRequest, DTOGetKeygenDataRequest, DTOGetKeygenDataResponse
from pydantic import EmailStr


router = APIRouter(prefix="/keys",
                   tags=["Keys"],
                   responses={},
                   dependencies=[])



@router.get("/", status_code=status.HTTP_200_OK)
def keys_get_keys_data(
    payload: DTOGetKeygenDataRequest,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = KeysService(dbconn)
        controller = KeysController()

        model = service.get_data(payload=payload)
        response = controller.validate_response(model=model, DTO=DTOGetKeygenDataResponse)
        return response
    except BusinessError as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from keys"
        )




@router.post("/", status_code=status.HTTP_201_CREATED)
def keys_post_new_key(
    payload: DTONewKeygenRequest,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = KeysService(dbconn)
        controller = KeysController()

        model = service.register(payload=payload)
        response = controller.validate_response(model=model, DTO=DTOGetKeygenDataResponse)
        return response
    except BusinessError as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from keys"
        )




@router.delete("/{key_text}", status_code=status.HTTP_204_NO_CONTENT)
def keys_delete_key(
    key_text: UUID,
    payload: DTOUserAndPassword,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = KeysService(dbconn)
        service.delete(payload=dict(user_email=payload.user_email,
                                    password=payload.password,
                                    key_text=key_text))
    except BusinessError as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from keys"
        )

    return None