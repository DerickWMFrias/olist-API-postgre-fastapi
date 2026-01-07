from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from uuid import UUID

class DTOUserPatch(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    recovery_email: EmailStr | None = None

    @model_validator(mode="after")
    def at_least_one_field_present(self):
        if not any([
            self.email,
            self.password,
            self.recovery_email,
        ]):
            raise ValueError(
                "At least one field must be provided: email, password or recovery_email"
            )
        return self


class DTOUserRegister(BaseModel):
    email: EmailStr
    password: str
    recovery_email: EmailStr

class DTOUserGetData(BaseModel):
    user_id: UUID
    email: EmailStr
    #hashed_password: str
    recovery_email: EmailStr

    model_config = ConfigDict(from_attributes=True)

    
class DTOUserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

