import datetime
import time

from authlib.jose import jwt, RSAKey
from authlib.jose.errors import BadSignatureError
from fastapi import Request
from starlette.types import ASGIApp, Scope, Receive, Send

from app.core.exceptions import AuthException


class AuthMiddleware:
    _IGNORE_PATHS = {
        "/health",
    }

    def __init__(self, app: ASGIApp, public_key: RSAKey) -> None:
        self._app = app
        self._public_key = public_key

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not scope.get("path") or scope["path"] in self._IGNORE_PATHS:
            await self._app(scope, receive, send)
            return

        request = Request(scope=scope, receive=receive, send=send)
        auth_header = request.headers.get("x-auth-header")

        if not auth_header:
            raise AuthException(message="There is not x-auth-header")

        try:
            token = jwt.decode(auth_header, self._public_key)
        except BadSignatureError:
            raise AuthException(message='Bad jwt token signature')

        exp = token.get("exp")
        if exp < datetime.datetime.now().timestamp():
            raise AuthException(message="Jwt token expired")

        scope.setdefault("extensions", {})["username"] = token["username"]

        await self._app(scope, receive, send)
