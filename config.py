import os
from dotenv import load_dotenv
from dataclasses import dataclass



@dataclass
class Config:
    admin_password: str
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'games.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def load_config() -> Config:
    load_dotenv()
    return Config(admin_password=os.environ.get('ADMIN_PASSWORD'))
