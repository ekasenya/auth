from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse

from .exceptions import AuthException


def auth_exception_handler(_: Request, exc: AuthException):
    return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content=exc.message)
