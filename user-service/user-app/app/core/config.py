import os


class Config:
    AUTH_PUBLIC_KEY: str = ""
    APP_NAME = os.environ.get("APP_NAME")


config = Config()
