from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.exceptions import AuthException


def default_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, AuthException):
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content=exc.message)
    else:
        return JSONResponse(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=exc.message)
