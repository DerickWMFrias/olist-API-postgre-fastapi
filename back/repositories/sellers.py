from models.schemas import Seller
from typing import List
import uuid
from repositories.geolocation import GeolocationRepository
from errors.errors import NotFoundError, BadRequestError
from .geolocation import GeolocationRepository

class SellerRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_seller_data_by_id(self, seller_id: uuid.UUID) -> Seller:
        try:
            seller = self.dbconn.get(Seller, seller_id)
        except Exception as e:
            raise e
        return seller
    
    def get_sellers_by_id_list(self, list_seller_id: list[uuid.UUID]) -> list[Seller]:
        list_sellers = []
        try:
            for seller_id in list_seller_id:
                seller = self.get_seller_data_by_id(seller_id=seller_id)
                list_sellers.append(seller)
        except Exception as e:
            raise e
        
        return list_sellers


    def update_seller_zipcode_prefix(self, seller_id: uuid.UUID, zip_code_prefix: str) -> Seller:
        try:
            seller: Seller = self.dbconn.get(Seller, seller_id)
            if not seller:
                raise NotFoundError(err_msg="Seller not found.",
                                    log_msg="Seller not found.")
            

            geolocation_repository = GeolocationRepository(db=self.dbconn)
            geolocation = geolocation_repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=zip_code_prefix)
            if not geolocation:
                raise BadRequestError(err_msg="Bad zipcode prefix",
                                      log_msg=f"Could not find zipcode prefix {zip_code_prefix}")


            seller.seller_zip_code_prefix= zip_code_prefix
            seller.seller_city = geolocation.geolocation_city
            seller.seller_state = geolocation.geolocation_state
            self.dbconn.commit()
            self.dbconn.refresh(seller)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return seller

    def add_new_seller(self, zip_code_prefix: str) -> Seller:
        try:
            geo_repository = GeolocationRepository(self.dbconn)
            geolocation = geo_repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=zip_code_prefix)

            new_seller = Seller(
                seller_id= uuid.uuid4(),
                seller_zip_code_prefix=zip_code_prefix,
                seller_city=geolocation.geolocation_city,
                seller_state=geolocation.geolocation_state
            )

            self.dbconn.add(new_seller)
            self.dbconn.commit()
            self.dbconn.refresh(new_seller)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_seller
    

    def get_seller_data_by_zipcode_prefix(self, limit: int, cursor: uuid.UUID | None, zip_code_prefix: str) -> tuple[list[Seller], uuid.UUID | None]:
        try:
            if not zip_code_prefix:
                query = (
                    self.dbconn
                    .query(Seller)
                    .order_by(Seller.seller_id)
                )
            else:
                query = (
                    self.dbconn
                    .query(Seller)
                    .filter(Seller.seller_zip_code_prefix == zip_code_prefix)
                    .order_by(Seller.seller_id)
                )

            # Filtra por cursor
            if cursor:
                cursor_uuid = uuid.UUID(cursor)
                query = query.filter(
                    Seller.seller_id > cursor_uuid
                )

            results = query.limit(limit + 1).all()


            # Filtra se ha resultados p/ busca
            if not results:
                raise BadRequestError(err_msg="Cant process sent cursor",
                                        log_msg="Cant process sent cursor")


            # Gera proximo cursor
            has_next = len(results) > limit
            items = results[:limit]

            next_cursor = None
            if has_next:
                last = items[-1]
                next_cursor = str(last.coordinate_id)

        except Exception as e:
            raise e
        
        return items, next_cursor