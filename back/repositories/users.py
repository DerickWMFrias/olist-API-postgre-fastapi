from models.schemas import User
import uuid
from lib.bcrypt import BcryptService
from pydantic import EmailStr
from models.dtos import DTOUserPatch
from errors.errors import BadRequestError
class UserRepository:
    def __init__(self, db):
        self.dbconn = db
        self.bcrypt_service = BcryptService()

    def get_user_data_by_user_id(self, user_id: uuid.UUID) -> User:
        try:
            user = self.dbconn.query(User).filter(User.user_id == user_id).first()

            if not user:
                raise BadRequestError(err_msg="",
                                      log_msg="Bad user_id")
        except Exception as e:
            raise e        
        return user


    def get_user_data_by_email(self, user_email: EmailStr) -> User:
        try:
            user = self.dbconn.query(User).filter(User.email == user_email).first()
        except Exception as e:
            raise e        
        return user
    
    def auth_user_email_and_password(self, user_email: EmailStr, password: str):
        try:
            user = self.get_user_data_by_email(user_email=user_email)
            if not user:
                return False, None

            password_ok = self.bcrypt_service.compare_passwords_bcrypt(password1=password,
                                                                        password2=user.hashed_password)        
            if not password_ok:
                return False, None
        except Exception as e:
            raise e
        
        return True, user
    
    def register_user(self, email: EmailStr, hashed_password: str, recovery_email: EmailStr) -> User:
        try:
            new_user = User(
                user_id=uuid.uuid4(),
                email=email,
                hashed_password=hashed_password,
                recovery_email=recovery_email
            )

            # 4. ADD NO BANCO
            self.dbconn.add(new_user)
            self.dbconn.commit()
            self.dbconn.refresh(new_user)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_user

    def patch_user_by_user_id(self, user_id: uuid.UUID, payload: DTOUserPatch) -> User | None:
        try:
            user = self.get_user_data_by_user_id(user_id=user_id)

            if not user:
                return None

            if payload.email is not None:
                user.email = payload.email

            if payload.recovery_email is not None:
                user.recovery_email = payload.recovery_email

            if payload.password is not None:
                user.hashed_password = self.bcrypt_service.hash_password(password=payload.password)

            self.dbconn.commit()
            self.dbconn.refresh(user)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return user
    
    def delete_user(self, user_id: uuid.UUID) -> User | None:
        try:
            rows_deleted = (
                self.dbconn
                .query(User)
                .filter(User.user_id == user_id)
                .delete(synchronize_session=False)
            )
            self.dbconn.commit()
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return rows_deleted