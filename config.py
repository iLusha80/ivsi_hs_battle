import os
from dotenv import load_dotenv
from dataclasses import dataclass

basedir = os.path.abspath(os.path.dirname(__file__))

@dataclass
class Config:
    admin_password: str
    SECRET_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    SQLALCHEMY_DATABASE_URI: str  # Вычисляется в load_config
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TELEGRAM_BOT_TOKEN: str = None

def load_config() -> Config:
    load_dotenv()
    postgres_user = os.environ.get('POSTGRES_USER')
    postgres_password = os.environ.get('POSTGRES_PASSWORD')
    postgres_host = os.environ.get('POSTGRES_HOST')
    postgres_port = os.environ.get('POSTGRES_PORT', '5432')       # Значение по умолчанию
    postgres_db = os.environ.get('POSTGRES_DB')
    postgres_schema = os.environ.get('POSTGRES_SCHEMA')

    return Config(
        admin_password=os.environ.get('ADMIN_PASSWORD'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        POSTGRES_USER=postgres_user,
        POSTGRES_PASSWORD=postgres_password,
        POSTGRES_HOST=postgres_host,
        POSTGRES_PORT=postgres_port,
        POSTGRES_DB=postgres_db,
        POSTGRES_SCHEMA=postgres_schema,
        SQLALCHEMY_DATABASE_URI=f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}?options=-csearch_path%3D{postgres_schema}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TELEGRAM_BOT_TOKEN=os.environ.get('TELEGRAM_BOT_TOKEN')
    )