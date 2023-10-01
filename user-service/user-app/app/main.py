from typing import Optional

import uvicorn
from authlib.jose import RSAKey
from fastapi import FastAPI, Depends, status, Response
from sqlalchemy.exc import IntegrityError

from app.core.config import config
from app.core.deps import get_user_repository, get_username
from app.core.exception_handlers import default_exception_handler
from app.middleware.auth import AuthMiddleware
from app.middleware.prometheus import metrics, PrometheusMiddleware
from app.repositories.user_repository import UserRepository
from app.schemas.user import User, UserUpdate

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name=config.APP_NAME)
app.add_middleware(AuthMiddleware, public_key=RSAKey.import_dict_key(config.AUTH_PUBLIC_KEY_DICT))
app.add_exception_handler(exc_class_or_status_code=Exception, handler=default_exception_handler)
app.add_route("/metrics", metrics)


@app.get('/')
async def root():
    return {"message": "Hi there"}


@app.get('/health')
async def check_health():
    return {"status": "OK"}


@app.post('/user', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_info: UserUpdate,
        response: Response,
        user_name: str = Depends(get_username),
        user_repository: UserRepository = Depends(get_user_repository),
):
    try:
        return await user_repository.create_user(
            user_name=user_name,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            email=user_info.email
        )
    except IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT


@app.get('/user/{user_id}', response_model=Optional[User])
async def get_user_by_id(
        user_id: int,
        response: Response,
        user_name: str = Depends(get_username),
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_user_by_id(
        user_id=user_id
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    if user.user_info.user_name != user_name:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    return user


@app.delete('/user/{user_id}', response_model=Optional[User])
async def get_user_by_id(
        user_id: int,
        response: Response,
        user_name: str = Depends(get_username),
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_user_by_id(
        user_id=user_id
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    if user.user_info.user_name != user_name:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    user = await user_repository.delete_user(
        user_id=user_id
    )

    return user


@app.put('/user/{user_id}', response_model=Optional[User])
async def update_user_by_id(
        user_id: int,
        user_update: UserUpdate,
        response: Response,
        user_name: str = Depends(get_username),
        user_repository: UserRepository = Depends(get_user_repository),
):
    user = await user_repository.get_user_by_id(
        user_id=user_id
    )

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    if user.user_info.user_name != user_name:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    user = await user_repository.update_user(
        user_id=user_id,
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        email=user_update.email
    )

    return user


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info")