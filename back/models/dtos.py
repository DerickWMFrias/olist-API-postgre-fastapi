from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, Field
from uuid import UUID
from decimal import Decimal

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
    recovery_email: EmailStr

    model_config = ConfigDict(from_attributes=True)

    
class DTOUserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)




class DTOGeolocation(BaseModel):
    geolocation_zip_code_prefix: str = Field(max_length=8)
    geolocation_city: str
    geolocation_state: str

    model_config = ConfigDict(from_attributes=True)



class DTOCoordinates(BaseModel):
    geolocation_zip_code_prefix: str = Field(max_length=8)
    lat: Decimal
    lng: Decimal

    model_config = ConfigDict(from_attributes=True)