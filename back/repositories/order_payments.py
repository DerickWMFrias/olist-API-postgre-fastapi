from typing import List
from models.schemas import OrderPayment
import uuid
from errors.errors import BadRequestError

class OrderPaymentRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_order_payments_by_id(self, order_id: uuid.UUID) -> List[OrderPayment]:
        try:
            order_payments = self.dbconn.query(OrderPayment).filter(OrderPayment.order_id == order_id).all()

            if not order_payments:
                raise BadRequestError(err_msg="Bad order_id",
                                      log_msg="Bad order_id")
        except Exception as e:
            raise e
        return order_payments
    
    def add_order_payments(self, payments: List[OrderPayment]) -> List[OrderPayment]:
        try:
            self.dbconn.add_all(payments)
            self.dbconn.commit()

            for payment in payments:
                self.dbconn.refresh(payment)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return payments
    
    def delete_order_payments(self, order_id: uuid.UUID) -> None:
        pass