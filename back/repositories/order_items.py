from typing import List
from models.schemas import OrderItem
import uuid
from errors.errors import BadRequestError
class OrderItemRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_order_items_by_id(self, order_id: uuid.UUID) -> List[OrderItem]:
        try:
            order_items = self.dbconn.query(OrderItem).filter(OrderItem.order_id == order_id).all()

            if not order_items:
                raise BadRequestError(err_msg="Bad order_id",
                                      log_msg="Bad order_id")
        except Exception as e:
            raise e
        return order_items
    
    def add_order_item(self, order_items: List[OrderItem]) -> List[OrderItem]:
        try:
            self.dbconn.add_all(order_items)
            self.dbconn.commit()

            for item in order_items:
                self.dbconn.refresh(item)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return order_items
    
    def delete_order_item(self, order_id: uuid.UUID) -> None:
        pass