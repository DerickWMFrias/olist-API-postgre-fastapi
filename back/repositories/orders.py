from models.schemas import Order
import uuid

class OrderRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_order_data_by_id(self, order_id: uuid.UUID) -> Order:
        try:
            order = self.dbconn.get(Order, order_id)
        except Exception as e:
            raise e
        return order
    
    def add_order(self, new_order: Order) -> Order:
        try:
            self.dbconn.add(new_order)
            self.dbconn.commit()
            self.dbconn.refresh(new_order)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_order

    