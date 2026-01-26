from models.schemas import Coordinates
from errors.errors import BadRequestError, NotFoundError
from models.dtos import DTOCoordinates
import uuid

class CoordinatesRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_coordinates_data_by_coordinate_id(self, coordinate_id: uuid.UUID) -> Coordinates:
        try:
            coordinates = self.dbconn.get(Coordinates, coordinate_id)

            if not coordinates:
                raise NotFoundError(err_msg="No coordinate with such uuid",
                                    log_msg=f"Could not find coordinate with uuid {coordinate_id}")
        except Exception as e:
            raise e
        return coordinates
    

    def get_paginated_coordinates(self, limit: int, cursor: uuid.UUID | None, zipcode_prefix: str) -> tuple[list[Coordinates], uuid.UUID | None]:
        try:
            if not zipcode_prefix:
                query = (
                    self.dbconn
                    .query(Coordinates)
                    .order_by(Coordinates.coordinate_id)
                )
            else:
                query = (
                    self.dbconn
                    .query(Coordinates)
                    .filter(Coordinates.geolocation_zip_code_prefix == zipcode_prefix)
                    .order_by(Coordinates.coordinate_id)
                )

            # Filtra por cursor
            if cursor:
                cursor_uuid = uuid.UUID(cursor)
                query = query.filter(
                    Coordinates.coordinate_id > cursor_uuid
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
    
    def add_coordinate(self, new_coordinate: DTOCoordinates) -> Coordinates:
        try:
            new_coordinate = Coordinates(
                    coordinate_id=uuid.uuid4(),
                    geolocation_zip_code_prefix=new_coordinate.geolocation_zip_code_prefix,
                    lat=new_coordinate.lat,
                    lng=new_coordinate.lng
                )
                
            self.dbconn.add(new_coordinate)
            self.dbconn.commit()
            self.dbconn.refresh(new_coordinate)
        except Exception as e:
            raise e
        
        return new_coordinate
    

    def delete_coordinate(self, coordinate_id: uuid.UUID) -> Coordinates:
        try:
            rows_deleted = (
                self.dbconn
                .query(Coordinates)
                .filter(Coordinates.coordinate_id == coordinate_id)
                .delete(synchronize_session=False)
            )
            self.dbconn.commit()
            
        except Exception as e:
            raise e
        
        return rows_deleted