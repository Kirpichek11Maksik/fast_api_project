import datetime as dt
import os

import jwt

from schema.user import UserLoginSchema
from service.user_service import UserService
from excepction import UserNotFound, UserNotCorrectPassword

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_change_me")


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_service.get_user_by_username(username)
        if not user:
            raise UserNotFound
        if user.password != password:
            raise UserNotCorrectPassword
        return UserLoginSchema(
            user_id=user.id,
            access_token=self.generate_access_token(user.id),
        )

    def register(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_service.create_user(username, password)
        return UserLoginSchema(
            user_id=user.id,
            access_token=self.generate_access_token(user.id),
        )

    @staticmethod
    def generate_access_token(user_id: int) -> str:
        expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=7)
        payload = {"user_id": user_id, "exp": expires}
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")