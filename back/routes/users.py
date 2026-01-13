import logging
from dbconfig.conn import get_dbconn
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.dtos import DTOUserRegister
from controllers.controllers import UserController
from services.users import UserService
from sqlalchemy.orm import Session
from uuid import UUID
from errors.errors import NotFoundError, EmailAlreadyRegisteredError, UnauthorizedError
from models.dtos import DTOUserResponse, DTOUserGetData, DTOUserPatch
from pydantic import EmailStr
from lib.api_validation import validate_api_key


router = APIRouter(prefix="/users",
                   tags=["Users"],
                   responses={},
                   dependencies=[Depends(validate_api_key)])



@router.get("/", status_code=200) #200: OK  401: Unauthorized  500: Internal Error
def users_get_user(
    email: EmailStr = Query(..., description="Email de login do usuário"),
    password: str = Query(..., description="Senha de login do usuário"),
    full_data: bool = False,
    dbconn: Session = Depends(get_dbconn),
    ):
    try:
        service = UserService(dbconn)
        controller = UserController()

        user = service.get_user_data(email=email,
                                     password=password)

        if full_data:
            response = controller.validate_response(model=user,
                                        DTO=DTOUserGetData)
        else:
            response = controller.validate_response(model=user,
                                                    DTO=DTOUserResponse)
            
        return response
    except UnauthorizedError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting data from user"
        )
    




@router.post("/", status_code=201)
def users_register_user(
    payload: DTOUserRegister,
    dbconn: Session = Depends(get_dbconn),
    ):
    try:
        service = UserService(dbconn)
        controller = UserController()

        new_user = service.register_user(payload)
        response = controller.validate_response(model=new_user,
                                                DTO=DTOUserResponse)
        return response
    except EmailAlreadyRegisteredError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )
    


@router.patch("/{user_id}", status_code=200)
def users_patch_user(
    user_id: UUID,
    payload: DTOUserPatch,
    dbconn: Session = Depends(get_dbconn),
    #user_id: UUID = Query(..., description="O UUID do usuário"),
    ):
    try:
        service = UserService(dbconn)
        controller = UserController()

        user = service.patch_user(user_id=user_id, payload=payload)

        response = controller.validate_response(
            model=user,
            DTO=DTOUserGetData
        )
        return response

    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error patching data from user"
        )
    


@router.delete("/{user_id}", status_code=204) #204: No Content or 404 Not Found or 500 Server Error
def users_delete_user(
    user_id: UUID,
    dbconn: Session = Depends(get_dbconn),
    ):
    try:
        service = UserService(dbconn)
        service.delete_user(user_id=user_id)
    except NotFoundError:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
    
    return None
