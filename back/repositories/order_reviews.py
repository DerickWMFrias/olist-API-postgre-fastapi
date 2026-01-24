from typing import List
from models.schemas import OrderReview
import uuid

class OrderReviewRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_reviews_by_order_id(self, order_id: uuid.UUID) -> List[OrderReview]:
        try:
            reviews = self.dbconn.query(OrderReview).filter(OrderReview.order_id == order_id).all()
        except Exception as e:
            raise e
        return reviews
    
    def get_review_by_review_id(self, review_id: uuid.UUID) -> OrderReview:
        try:
            review = self.dbconn.get(OrderReview, review_id)
        except Exception as e:
            raise e
        return review
    
    def edit_review_by_review_id(self, review_id: uuid.UUID, new_review_title: str | None = None, new_review_text: str | None = None) -> OrderReview:
        pass