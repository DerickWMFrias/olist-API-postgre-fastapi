from typing import List
from models.schemas import Customer
import uuid
from repositories.geolocation import GeolocationRepository

class CustomerRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_customer_data_by_id(self, customer_id: uuid.UUID) -> Customer:
        try:
            customer = self.dbconn.get(Customer, customer_id)
        except Exception as e:
            raise e
        return customer
    
    def get_customer_data_by_zipcode_prefix(self, zip_code_prefix: str) -> List[Customer]:
        pass

    def update_customer_zipcode_prefix(self, customer_id: uuid.UUID, zip_code_prefix: str) -> Customer:
        pass

    def add_new_customer(self, zip_code_prefix: str) -> Customer:
        try:
            geo_repository = GeolocationRepository(self.dbconn)
            geolocation = geo_repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=zip_code_prefix)

            new_customer = Customer(
                customer_id= uuid.uuid4(),
                customer_unique_id= uuid.uuid4(),
                customer_zip_code_prefix=zip_code_prefix,
                customer_city=geolocation.geolocation_city,
                customer_state=geolocation.geolocation_state
            )

            self.dbconn.add(new_customer)
            self.dbconn.commit()
            self.dbconn.refresh(new_customer)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_customer