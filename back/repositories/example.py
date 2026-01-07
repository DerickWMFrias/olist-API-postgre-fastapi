# src/repositories/user_repository.py
from models.example import User

class UserRepository:
    def get_by_id(self, user_id: int) -> User:
        pass
        # Aqui dentro você usaria o SQLAlchemy, Motor, etc.
        # Exemplo hipotético:
        user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        return User(**user_data) # Transforma o dado do banco no Model