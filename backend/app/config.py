import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # JWT 配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Access token 1小時過期
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token 30天過期

    DEBUG = True
