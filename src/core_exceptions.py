class BaseAPIException(Exception):
    detail = NotImplemented
    status_code = NotImplemented
    description = NotImplemented

    def __init__(self, detail: str = None, status_code: int = None, description: str = None):
        self.detail = detail or self.__class__.detail
        self.status_code = status_code or self.__class__.status_code
        self.description = description or self.__class__.description

    def response(self) -> dict:
        return {
            self.status_code: {
                "description": self.description,
                "content": self.content,
            }
        }

    @property
    def content(self):
        return {"application/json": {"example": {"detail": self.detail}}}

    def example(self) -> dict:
        return {self.description: {"value": {"detail": self.detail}}}


class BadRequestsException(BaseAPIException):
    status_code = 400
    detail = "Bad Request"


class UnauthorizedException(BaseAPIException):
    status_code = 401
    detail = "Unauthorized"


class PermissionDenied(BaseAPIException):
    status_code = 403
    detail = "Permission Denied"


class NotFoundException(BaseAPIException):
    status_code = 404
    detail = "Object Not found"
