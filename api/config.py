from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    USER_INSERT: str
    GIT_TOKEN: str
    YAGMAIL_USERNAME: str
    YAGMAIL_PASSWORD: str

    class Config:
        env_file = '.env'


settings = Settings()
