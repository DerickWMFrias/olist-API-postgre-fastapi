import logging
from errors.errors import UnauthorizedError
from pydantic import BaseModel
from interfaces import InterfaceService
from typing import Dict
from repositories.users import UserRepository
from repositories.keys import KeysRepository

logger = logging.getLogger(__name__)


class KeysService(InterfaceService):
    def __init__(self, db):
        self.dbconn = db
        self.repository = KeysRepository(db=db)

    def get_data(self, payload:  Dict | BaseModel):
        try:
            user_repository = UserRepository(self.dbconn)
            is_auth, _ = user_repository.auth_user_email_and_password(user_email=payload.user_email,
                                                                   password=payload.password)
            if not is_auth:
                raise UnauthorizedError(
                    err_msg="Invalid credentials",
                    log_msg="Password mismatch"
                )


            key = self.repository.get_key_data_by_key_text(key_text=payload.key_text)
            if not key:
                raise UnauthorizedError(
                    err_msg="Invalid credentials",
                    log_msg="Key_text mismatch"
                )
            
        except Exception as e:
            raise e
        
        return key
    

    def register(self, payload:  Dict | BaseModel):
        try:
            user_repository = UserRepository(self.dbconn)
            is_auth, user = user_repository.auth_user_email_and_password(user_email=payload.user_email,
                                                                   password=payload.password)
            if not is_auth:
                raise UnauthorizedError(
                    err_msg="Invalid credentials",
                    log_msg="Password mismatch"
                )

            new_key = self.repository.register_key(user_id=user.user_id)
        except Exception as e:
            raise e
        
        return new_key
    
    def patch(self, payload: Dict | BaseModel):
        return super().patch(payload)
    

    def delete(self, payload: Dict | BaseModel):
        try:
            user_repository = UserRepository(self.dbconn)
            is_auth, _ = user_repository.auth_user_email_and_password(user_email=payload.user_email,
                                                                   password=payload.password)
            if not is_auth:
                raise UnauthorizedError(
                    err_msg="Invalid credentials",
                    log_msg="Password mismatch"
                )

            self.repository.delete_key(key_text=payload.key_text)
        except Exception as e:
            raise e