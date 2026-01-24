from models.schemas import Seller
from typing import List
import uuid
from repositories.geolocation import GeolocationRepository

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

    def get_seller_data_by_zipcode_prefix(self, zip_code_prefix: str) -> List[Seller]:
        pass

    def update_seller_zipcode_prefix(self, seller_id: uuid.UUID, zip_code_prefix: str) ->Seller:
        pass

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