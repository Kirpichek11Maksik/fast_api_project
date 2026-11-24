import secrets
from repository.user_repository import UserRepository
from dataclasses import dataclass
from schema.user import UserLoginSchema

@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token: str = self.generate_access_token()
        user = self.user_repository.create_user(username, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def generate_access_token() -> str:
        return secrets.token_urlsafe(10)