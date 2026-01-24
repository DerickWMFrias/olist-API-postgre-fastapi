from models.schemas import Geolocation
from models.dtos import DTOGeolocation

class GeolocationRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_geolocation_data_by_zipcode_prefix(self, zip_code_prefix: str) -> Geolocation:
        try:
            geolocation = self.dbconn.get(Geolocation, zip_code_prefix)
        except Exception as e:
            raise e
        return geolocation
    
    def add_geolocation(self, new_geolocation: DTOGeolocation) -> Geolocation:
        try:
            new_geolocation = Geolocation(
                geolocation_zip_code_prefix=new_geolocation.geolocation_zip_code_prefix,
                geolocation_city=new_geolocation.geolocation_city,
                geolocation_state=new_geolocation.geolocation_state
            )

            # 4. ADD NO BANCO
            self.dbconn.add(new_geolocation)
            self.dbconn.commit()
            self.dbconn.refresh(new_geolocation)
        except Exception as e:
            self.dbconn.rollback()
            raise e

        return new_geolocation
        
    def delete_geolocation(self, zipcode_prefix: str) -> Geolocation | None:
        try:
            rows_deleted = (
                    self.dbconn
                    .query(Geolocation)
                    .filter(Geolocation.geolocation_zip_code_prefix == zipcode_prefix)
                    .delete(synchronize_session=False)
                )
            self.dbconn.commit()
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return rows_deleted