from sqlalchemy import select, exists
from models.schemas import Products
import uuid
from errors.errors import NotFoundError

class ProductRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_product_by_id(self, product_id: uuid.UUID) -> Products:
        try:
            product = self.dbconn.get(Products, product_id)

            if not product:
                raise NotFoundError(err_msg="Bad product_id",
                                    log_msg="Bad product_id")
        except Exception as e:
            raise e
        
        return product

    def get_products_by_id_list(self, list_product_id: list[uuid.UUID]) -> list[Products]:
        products = []
        try:
            for product_id in list_product_id:
                product = self.get_product_by_id(product_id=product_id)
                products.append(product)
        except Exception as e:
            raise e
        
        return products

    def add_product(self, new_product: Products) -> Products:
        try:
            self.dbconn.add(new_product)
            self.dbconn.commit()
            self.dbconn.refresh(new_product)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_product
    
    def is_product_id_in_table(self, product_id: uuid.UUID) -> bool:
        try:
            stmt = select(exists().where(Products.product_id == product_id))
        except Exception as e:
            raise e
        return self.dbconn.execute(stmt).scalar()
    
    def delete_product_by_product_id(self, product_id: uuid.UUID) -> None:
        pass