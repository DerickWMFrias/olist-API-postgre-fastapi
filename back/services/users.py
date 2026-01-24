import logging
from models.dtos import DTOUserRegister, DTOUserPatch
from models.schemas import User
from errors.errors import EmailAlreadyRegisteredError, NotFoundError, UnauthorizedError
from uuid import UUID
from pydantic import EmailStr
from repositories.users import UserRepository
from lib.bcrypt import BcryptService

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db):
        self.dbconn = db
        self.repository = UserRepository(db=db)
        self.bcrypt_service = BcryptService()

    def is_user_credentials_valid(self, email: EmailStr, password: str) -> bool:
        return self.repository.auth_user_email_and_password(user_email=email, password=password)
    
    def get_user_data(self, email: EmailStr, password: str) -> User:
        try:
            is_auth, user = self.repository.auth_user_email_and_password(user_email=email, 
                                                                        password=password)
            if not is_auth:
                raise UnauthorizedError(
                    err_msg="Invalid credentials",
                    log_msg="Password mismatch"
                )
        except Exception as e:
            raise e

        return user


    def patch_user(self, user_id: UUID, payload: DTOUserPatch) -> User:
        try:
            user = self.repository.patch_user_by_user_id(user_id=user_id, 
                                                         payload=payload)
            if not user:
                raise NotFoundError(
                    err_msg="User not found",
                    log_msg=f"User {user_id} not found"
                )
        except Exception as e:
            raise e

        return user


    def register_user(self, dto: DTOUserRegister) -> User:
        try:
            # 1. VERIFICA SE USUARIO JA NAO ESTA REGISTRADO
            user_exists = self.repository.get_user_data_by_email(user_email=dto.email)
            if user_exists:
                raise EmailAlreadyRegisteredError


            hashed_password = self.bcrypt_service.hash_password(password=dto.password)


            # 3. SALVA NO BANCO
            new_user = self.repository.register_user(email=dto.email,
                                                    hashed_password=hashed_password,
                                                    recovery_email=dto.recovery_email)
            
            logging.debug(f"Successful register of user w/ email {dto.email}")
        except Exception as e:
            raise e
    
        return new_user
    

    

    def delete_user(self, user_id: UUID):
        try:
            rows_deleted = self.repository.delete_user(user_id=user_id)
            if not rows_deleted:
                raise NotFoundError(err_msg="User not found.",
                                    log_msg="User not found.")
        except Exception as e:
            raise e
