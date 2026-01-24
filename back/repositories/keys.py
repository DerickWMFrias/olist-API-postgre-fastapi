from models.schemas import Keys
import uuid
from datetime import datetime, timedelta, timezone

class KeysRepository:
    def __init__(self, db):
        self.dbconn = db

    def get_key_by_validate_key_text(self, key_text: uuid.UUID) -> Keys:
        try:
            key = self.dbconn.query(Keys).filter(Keys.key_text == key_text).first()
        except Exception as e:
            raise e
        
        return key
    
    def register_key(self, user_id: uuid.UUID) -> Keys:
        try:
            now = datetime.now(timezone.utc)
            new_key = Keys(
                user_id = user_id,
                key_text = uuid.uuid4(),
                created_at_tmzone = now,
                expires_at_tmzone = now + timedelta(weeks=1)
            )

            self.dbconn.add(new_key)
            self.dbconn.commit()
            self.dbconn.refresh(new_key)
        except Exception as e:
            self.dbconn.rollback()
            raise e
        
        return new_key
    
    def delete_key(self, key_todel: Keys) -> None:
        try:
            key_todel.is_revoked = True
            self.dbconn.commit()
            self.dbconn.refresh(key_todel)
        except Exception as e:
            self.dbconn.rollback()
            raise e