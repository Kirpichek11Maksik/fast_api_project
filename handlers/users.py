from typing import Annotated
from depency import get_user_service
from service.user import UserService
from fastapi import APIRouter, Depends
from schema.user import UserCreateSchema, UserLoginSchema
router = APIRouter(prefix="/user", tags=["user"])



@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)

