from dataclasses import dataclass
from schema.user import UserLoginSchema
@dataclass
class AuthService:

    def login(self, username: str, password: str) -> UserLoginSchema:
        pass
