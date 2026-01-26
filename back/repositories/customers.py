from typing import List
from models.schemas import Customer
import uuid
from repositories.geolocation import GeolocationRepository
from errors.errors import NotFoundError, BadRequestError
from .geolocation import GeolocationRepository

class CustomerRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_customer_data_by_id(self, customer_id: uuid.UUID) -> Customer:
        try:
            customer = self.dbconn.get(Customer, customer_id)

            if not customer:
                raise NotFoundError(err_msg="Customer not found.",
                                    log_msg="Customer not found.")
        except Exception as e:
            raise e
        return customer
    

    def update_customer_zipcode_prefix(self, customer_id: uuid.UUID, zip_code_prefix: str) -> Customer:
        try:
            customer = self.get_customer_data_by_id(customer_id=customer_id)


            geolocation_repository = GeolocationRepository(db=self.dbconn)
            geolocation = geolocation_repository.get_geolocation_data_by_zipcode_prefix(zip_code_prefix=zip_code_prefix)


            customer.customer_zip_code_prefix = zip_code_prefix
            customer.customer_city = geolocation.geolocation_city
            customer.customer_state = geolocation.geolocation_state
            self.dbconn.commit()
            self.dbconn.refresh(customer)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return customer

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

    def get_customer_data_by_zipcode_prefix(self, limit: int, cursor: uuid.UUID | None, zip_code_prefix: str) -> tuple[list[Customer], uuid.UUID | None]:
        try:
            if not zip_code_prefix:
                query = (
                    self.dbconn
                    .query(Customer)
                    .order_by(Customer.customer_id)
                )
            else:
                query = (
                    self.dbconn
                    .query(Customer)
                    .filter(Customer.customer_zip_code_prefix == zip_code_prefix)
                    .order_by(Customer.customer_id)
                )

            # Filtra por cursor
            if cursor:
                cursor_uuid = uuid.UUID(cursor)
                query = query.filter(
                    Customer.customer_id > cursor_uuid
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