from typing import List
from models.schemas import OrderItem
import uuid

class OrderItemRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_order_items_by_id(self, order_id: uuid.UUID) -> List[OrderItem]:
        try:
            order_item = self.dbconn.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        except Exception as e:
            raise e
        return order_item
    
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