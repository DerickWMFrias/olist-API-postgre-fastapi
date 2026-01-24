from dbconfig.conn import get_dbconn
from fastapi import APIRouter, Depends, HTTPException, status
from controllers.controllers import OrderController
from services.orders import OrderService
from sqlalchemy.orm import Session
from errors.errors import BusinessError
from models.dtos import DTOCreateNewOrderRequest, DTOOrderID
from lib.api_validation import validate_api_key
import uuid

router = APIRouter(prefix="/order",
                   tags=["Orders"],
                   responses={},
                   dependencies=[Depends(validate_api_key)])


@router.get("/", status_code=status.HTTP_200_OK)
def orders_get_order_data(
    order_id: uuid.UUID,
    with_customer_data: bool = False,
    with_items_data: bool = False,
    with_payment_data: bool = False,
    with_seller_data: bool = False,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = OrderService(dbconn)
        controller = OrderController()

        order = service.get_data(payload=dict(order_id=order_id,
                                         with_customer_data=with_customer_data,
                                         with_items_data=with_items_data,
                                         with_payment_data=with_payment_data,
                                         with_seller_data=with_seller_data))
        response = controller.validate_response_getorder(model=order)
        return response
    except BusinessError as e:
        raise e
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )



@router.post("/", status_code=status.HTTP_201_CREATED)
def orders_post_order(
    payload: DTOCreateNewOrderRequest,
    dbconn: Session = Depends(get_dbconn),
):
    try:
        service = OrderService(dbconn)
        controller = OrderController()

        new_order = service.register(payload=payload)
        response = controller.validate_response(model=new_order,
                                                DTO=DTOOrderID)
        return response
    except BusinessError as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error posting order data"
        )
    
