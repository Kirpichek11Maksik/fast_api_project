from sqlalchemy import select
from sqlalchemy.orm import Session
from models import UserProfile


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str) -> UserProfile:
        user = UserProfile(username=username, password=password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user(self, user_id: int) -> UserProfile | None:
        return self.session.scalar(
            select(UserProfile).where(UserProfile.id == user_id)
        )

    def get_user_by_username(self, username: str) -> UserProfile | None:
        return self.session.scalar(
            select(UserProfile).where(UserProfile.username == username)
        )