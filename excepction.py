class UserNotFound(Exception):
    detail = "User not found"

class UserNotCorrectPassword(Exception):
    detail = "Не правильно введен пороль или нету такого пользователя"
