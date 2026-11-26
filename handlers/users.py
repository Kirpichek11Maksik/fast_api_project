from typing import Annotated
from depency import get_user_service
from excepction import UserNotCorrectPassword, UserNotFound
from service.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException
from schema.user import UserCreateSchema, UserLoginSchema
from service.auth_service import AuthService
from depency import get_auth_service


router = APIRouter(prefix="/user", tags=["user"])




@router.post("/create_user", response_model=UserLoginSchema)
def create_user(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_service.register(body.username, body.password)


@router.post("/login", response_model=UserLoginSchema)
def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except UserNotCorrectPassword:
        raise HTTPException(status_code=401, detail="Incorrect password")