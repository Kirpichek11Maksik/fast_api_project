class AppException(Exception):
    status_code = 400
    detail = "Error"

class UserNotFound(AppException):
    status_code = 404
    detail = "User not found"

class UserNotCorrectPassword(AppException):
    status_code = 401
    detail = "Неправильный логин или пароль"

class TokenNoCorrect(AppException):
    status_code = 401
    detail = "Токен некорректен"

class TokenHasExpired(AppException):
    status_code = 401
    detail = "Токен истёк"


class DeviceNotFound(AppException):
    status_code = 404
    detail = "Девайс не найден"