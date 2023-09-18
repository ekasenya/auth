from sqlalchemy import String, Table, Column, Integer

from .metadata import metadata

users = Table(
    "users",
    metadata,
    Column("username", Integer, primary_key=True),
    Column("password", String, unique=False, nullable=False),
)
