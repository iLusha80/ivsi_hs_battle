import os
from dotenv import load_dotenv
from dataclasses import dataclass



@dataclass
class Config:
    admin_password: str

def load_config() -> Config:
    load_dotenv()
    return Config(admin_password=os.environ.get('ADMIN_PASSWORD'))
