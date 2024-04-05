from core_exceptions import BaseAPIException
from core_exceptions import PermissionDenied as PermissionDeniedBase
from core_exceptions import UnauthorizedException as UnauthorizedExceptionBase


class PermissionDenied(PermissionDeniedBase):
    detail = "Permission Denied"
    description = "Not enough privileges"
    status_code = 403


class UnauthorizedException(UnauthorizedExceptionBase):
    detail = "Unauthorized"


class AuthLoginException(BaseAPIException):
    detail = "Incorrect username or password"
    description = ""
    status_code = 400


class InvalidToken(BaseAPIException):
    detail = "Invalid token"
    description = ""
    status_code = 400


class InvalidTokenType(InvalidToken):
    detail = "Invalid token type"
