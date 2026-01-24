import os
import bcrypt
import logging
import uuid
from models.dtos import DTOGeolocation, DTOCoordinates
from models.schemas import Keys, User
from errors.errors import ConflictError, NotFoundError, UnauthorizedError, BadRequestError
from fastapi import HTTPException
from pydantic import EmailStr, BaseModel
from interfaces import InterfaceService
from typing import Dict
from datetime import datetime, timedelta, timezone
from repositories.orders import OrderRepository
from repositories.customers import CustomerRepository
from repositories.order_items import OrderItemRepository
from repositories.order_payments import OrderPaymentRepository
from repositories.sellers import SellerRepository
from repositories.products import ProductRepository
from models.schemas import Order
from models.dtos import DTOCreateNewOrderRequest
logger = logging.getLogger(__name__)

__all__ = ["OrderService"]


class OrderService(InterfaceService):
    def __init__(self, db):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        self.repository = OrderRepository(db=db)
        self.dbconn = db


    def get_data(self, payload:  Dict | BaseModel):
        """
        return ret_dict: {
            "order": DTOOrder,
            "customer": DTOCustomer,
            "payments": List[DTOOrderPayments],
            "items": List[DTOItens]
        }
        em que DTOItens = {
            "item": DTOOrderItem,
            "product": DTOProduct,
            "seller": DTOSeller}
        """
        try:
            order = self.repository.get_order_data_by_id(order_id=payload["order_id"])

            ret_dict = {
                "order": order,
            }

            if payload["with_customer_data"]:
                customer_repository = CustomerRepository(db=self.dbconn)
                customer = customer_repository.get_customer_data_by_id(customer_id=order.customer_id)
                ret_dict["customer"] = customer

            if payload["with_payment_data"]:
                order_payments_repository = OrderPaymentRepository(db=self.dbconn)
                order_payments = order_payments_repository.get_order_payments_by_id(order_id=order.order_id)
                ret_dict["payments"] = order_payments

            if payload["with_items_data"]:
                items = make_items_list(payload=payload, 
                                       order_id=order.order_id,
                                       dbconn=self.dbconn)
                ret_dict["items"] = items
                
        except Exception as e:
            raise e
        
        return ret_dict
    

    def register(self, payload:  Dict | DTOCreateNewOrderRequest):
        try:
            new_order = self.repository.add_order(
                new_order=Order(
                    customer_id=payload.customer_id,
                    order_status=payload.order_status,
                    order_purchase_timestamp=payload.order_purchase_timestamp,
                    order_approved_at=payload.order_approved_at,
                    order_delivered_carrier_date=payload.order_delivered_carrier_date,
                    order_delivered_customer_date=payload.order_delivered_customer_date,
                    order_estimated_delivery_date=payload.order_estimated_delivery_date
            ))
        except Exception as e:
            raise e
        
        return new_order
    

    def patch(self, payload: Dict | BaseModel):
        return super().patch(payload)
    

    def delete(self, payload: Dict | BaseModel):
        return super().patch(payload)
    


def make_items_list(payload, order_id, dbconn):
    order_items_repository = OrderItemRepository(dbconn)
    products_repository = ProductRepository(dbconn)

    order_items = order_items_repository.get_order_items_by_id(order_id=order_id)


    # ---- 1. coletar IDs distintos dos produtos e dos sellers em order_items----
    product_ids = {item.product_id for item in order_items}

    seller_ids = set()
    if payload["with_seller_data"]:
        seller_ids = {item.seller_id for item in order_items}



    # ---- 2. bulk fetch dos dados dos IDS no banco----
    products = products_repository.get_products_by_id_list(
        list_product_id=list(product_ids)
    )

    products_map = {product.product_id: product for product in products}

    sellers_map = {}
    if payload["with_seller_data"]:
        seller_repository = SellerRepository(dbconn)
        sellers = seller_repository.get_sellers_by_id_list(
            list_seller_id=list(seller_ids)
        )
    sellers_map = {seller.seller_id: seller for seller in sellers}


    # ---- 3. montar resultado final ----
    items = []

    for item in order_items:
        item_data = {
            "item": item,
            "product": products_map.get(item.product_id),
        }

        if payload.get("with_seller_data"):
            item_data["seller"] = sellers_map.get(item.seller_id)

        items.append(item_data)

    return items