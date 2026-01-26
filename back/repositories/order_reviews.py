from typing import List
from models.schemas import OrderReview
import uuid
from errors.errors import BadRequestError, NotFoundError

class OrderReviewRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_reviews_by_order_id(self, order_id: uuid.UUID) -> List[OrderReview]:
        try:
            reviews = self.dbconn.query(OrderReview).filter(OrderReview.order_id == order_id).all()

            if not reviews:
                raise BadRequestError(err_msg="Bad order_id",
                                      log_msg="Bad order_id")
        except Exception as e:
            raise e
        return reviews
    
    def get_review_by_review_id(self, review_id: uuid.UUID) -> OrderReview:
        try:
            review = self.dbconn.get(OrderReview, review_id)

            if not review:
                raise NotFoundError(err_msg="Bad review_id",
                                    log_msg="Bad review_id")
        except Exception as e:
            raise e
        return review
    
    def edit_review_by_review_id(self, review_id: uuid.UUID, new_review_title: str | None = None, new_review_text: str | None = None) -> OrderReview:
        try:
            review = self.get_review_by_review_id(review_id=review_id)

            review.review_comment_title = new_review_title
            review.review_comment_message = new_review_text

            self.dbconn.commit()
            self.dbconn.refresh(review)
        except Exception as e:
            raise e
        return review