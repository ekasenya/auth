from typing import Optional

from app.models.user import users
from app.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository
from app.schemas.user import User
from sqlalchemy import insert, select, Row


class UserMapper:
    @staticmethod
    def row_to_user(row: Row):
        return User(
            username=row.username,
            password=row.password,
        )


class UserRepository(BaseSqlAlchemyRepository):
    async def create_user(
            self,
            user_name: str,
            password: str,
    ) -> User:
        insert_command = insert(users).values(
            username=user_name,
            password=password,
        ).returning(users)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(insert_command)).one()

        return UserMapper.row_to_user(row)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        select_command = select(users).where(users.c.username==username)

        async with self._db_connection.begin():
            row = (await self._db_connection.execute(select_command)).one_or_none()

        if not row:
            return None

        return UserMapper.row_to_user(row)