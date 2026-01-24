from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Literal

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
    coordinate_id: UUID | None = None
    geolocation_zip_code_prefix: str = Field(max_length=8)
    lat: Decimal
    lng: Decimal

    model_config = ConfigDict(from_attributes=True)


class DTOCoordinatesPaginated(BaseModel):
    items: list[DTOCoordinates]
    next_cursor: UUID | None



class DTOGetKeygenDataRequest(BaseModel):
    user_email: EmailStr
    password: str
    key_text: UUID



class DTOGetKeygenDataResponse(BaseModel):
    key_text: UUID
    is_expired: bool
    expires_at_tmzone: datetime

    model_config = ConfigDict(from_attributes=True)



class DTONewKeygenRequest(BaseModel):
    user_email: EmailStr
    password: str
    duration: datetime


class DTOUserAndPassword(BaseModel):
    user_email: EmailStr
    password: str



class DTOCreateNewOrderRequest(BaseModel):
    customer_id: UUID
    order_status: Literal["delivered", "invoiced", "shipped"]
    order_purchase_timestamp: datetime | None = None
    order_approved_at: datetime | None = None
    order_delivered_carrier_date: datetime | None = None
    order_delivered_customer_date: datetime | None = None
    order_estimated_delivery_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class DTOOrderID(BaseModel):
    order_id: UUID

    model_config = ConfigDict(from_attributes=True)


class DTOOrderItem(BaseModel):
    order_id: UUID
    order_item_id: int
    product_id: UUID
    seller_id: UUID
    shipping_limit_date: datetime | None
    price: Decimal
    freight_value: Decimal | None

    model_config = ConfigDict(from_attributes=True)


class DTOProduct(BaseModel):
    product_id: UUID
    product_category_name: str
    product_name_lenght: int | None
    product_description_lenght: int | None
    product_photos_qty: int | None
    product_weight_g: int | None
    product_length_cm: int | None
    product_height_cm: int | None
    product_width_cm: int | None

    model_config = ConfigDict(from_attributes=True)


class DTOSeller(BaseModel):
    seller_id: UUID
    seller_zip_code_prefix: str
    seller_city: str
    seller_state: str

    model_config = ConfigDict(from_attributes=True)


class DTOItemProductSeller(BaseModel):
    item: DTOOrderItem
    product: DTOProduct
    seller: DTOSeller | None

    model_config = ConfigDict(from_attributes=True)


class DTOOrder(BaseModel):
    order_id: UUID
    customer_id: UUID
    order_status: str
    order_purchase_timestamp: datetime | None
    order_approved_at: datetime | None
    order_delivered_carrier_date: datetime | None
    order_delivered_customer_date: datetime | None
    order_estimated_delivery_date: datetime | None

    model_config = ConfigDict(from_attributes=True)


class DTOCustomer(BaseModel):
    customer_id: UUID
    customer_unique_id: UUID
    customer_zip_code_prefix: str
    customer_city: str
    customer_state: str

    model_config = ConfigDict(from_attributes=True)


class DTOOrderPayments(BaseModel):
    order_id: UUID
    payment_sequential: int
    payment_type: str
    payment_installments: int
    payment_value: Decimal

    model_config = ConfigDict(from_attributes=True)


class DTOGetOrderResponse(BaseModel):
    order: DTOOrder
    customer: DTOCustomer
    payments: list[DTOOrderPayments] | None
    items: list[DTOItemProductSeller] | None

    model_config = ConfigDict(from_attributes=True)
    