import os
import bcrypt
import logging
from uuid import uuid4
from models.dtos import DTOUserRegister, DTOUserPatch
from models.schemas import User
from errors.errors import EmailAlreadyRegisteredError, NotFoundError, UnauthorizedError
from uuid import UUID
from fastapi import HTTPException
from pydantic import EmailStr

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.dbconn = db


    def get_user_data(self, email: EmailStr, password: str) -> User:
        user = self.dbconn.query(User).filter(User.email == email).first()
        if not user:
            raise UnauthorizedError(
                err_msg="Invalid credentials",
                log_msg="User not found"
            )
        
        password_ok = bcrypt.checkpw(
            password.encode("utf-8"),
            user.hashed_password.encode("utf-8")
        )

        if not password_ok:
            raise UnauthorizedError(
                err_msg="Invalid credentials",
                log_msg="Password mismatch"
            )

        return user


    def patch_user(self, user_id: UUID, payload: DTOUserPatch) -> User:
        user = self.dbconn.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise NotFoundError(
                err_msg="User not found",
                log_msg=f"User {user_id} not found"
            )

        if payload.email is not None:
            user.email = payload.email

        if payload.recovery_email is not None:
            user.recovery_email = payload.recovery_email

        if payload.password is not None:
            user.hashed_password = bcrypt.hashpw(
                payload.password.encode("utf-8"),
                bcrypt.gensalt(self.rounds)
            ).decode("utf-8")

        self.dbconn.commit()
        self.dbconn.refresh(user)

        return user


    def register_user(self, dto: DTOUserRegister) -> User:
        # 1. VERIFICA SE USUARIO JA NAO ESTA REGISTRADO
        user_exists = self.dbconn.query(User).filter(User.email == dto.email).first()
        if user_exists:
            raise EmailAlreadyRegisteredError

        # 2. GERA HASH DA SENHA
        hashed_password = bcrypt.hashpw(
            dto.password.encode("utf-8"),
            bcrypt.gensalt(self.rounds)
        ).decode("utf-8")

        # 3. SALVA NO BANCO
        new_user = User(
            user_id=uuid4(),
            email=dto.email,
            hashed_password=hashed_password,
            recovery_email=dto.recovery_email
        )

        # 4. ADD NO BANCO
        self.dbconn.add(new_user)
        self.dbconn.commit()
        self.dbconn.refresh(new_user)

        logging.debug(f"Successful register of user w/ email {dto.email}")
        return new_user
    

    

    def delete_user(self, user_id: UUID):
        rows_deleted = (
            self.dbconn
            .query(User)
            .filter(User.user_id == user_id)
            .delete(synchronize_session=False)
        )

        if not rows_deleted:
            raise NotFoundError(err_msg="User not found.",
                                log_msg="User not found.")
        
        self.dbconn.commit()
