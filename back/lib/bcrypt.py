import os
import bcrypt

class BcryptService:
    def __init__(self):
        self.rounds = int(os.getenv("BCRYPT_ROUNDS", "12"))
        
    def compare_passwords_bcrypt(self, password1: str, password2: str) -> bool:
        password_ok = bcrypt.checkpw(
                password1.encode("utf-8"),
                password2.encode("utf-8")
            )
        
        return password_ok
    
    def hash_password(self, password: str):
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(self.rounds)
        ).decode("utf-8")
        
        return hashed_password