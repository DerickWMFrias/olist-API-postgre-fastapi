from abc import ABC, abstractmethod
"""
Como definir Interfaces no Python?
Diferente de outras linguagens, o Python não tem a palavra-chave interface. Para isso, usamos Classes Abstratas (ABCs - Abstract Base Classes).
"""


# 1. Definimos a Interface (Contrato)
class UserRepository(ABC):
    
    @abstractmethod
    def save(self, user_data: dict):
        """Este método DEVE ser implementado pelas subclasses"""
        pass

# 2. Implementamos a Interface para o Postgres
class PostgresUserRepository(UserRepository):
    def save(self, user_data: dict):
        print(f"Salvando {user_data} no banco Postgres...")

# 3. Implementamos a Interface para o MongoDB
class MongoUserRepository(UserRepository):
    def save(self, user_data: dict):
        print(f"Salvando {user_data} no banco MongoDB...")


# Exemplo de injetancia:
class UserService:
    # O Service não sabe se o repo é Postgres ou Mongo. 
    # Ele só sabe que o objeto segue o contrato 'UserRepository'
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, data):
        # Regra de negócio aqui...
        return self.repo.save(data)