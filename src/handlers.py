
from typing import Type
from fastapi import Request
from fastapi.responses import JSONResponse


from core_exceptions import BaseAPIException


async def json_response_exception_handler(
    request: Request, exc: Type[BaseAPIException]
) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


exception_handlers = {
    BaseAPIException: json_response_exception_handler
}