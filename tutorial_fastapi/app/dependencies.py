# dependencies.py
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from .database import DatabaseAsync
from .config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()

settings = Settings.read_file()
secrets = Settings.read_file('tutorial_fastapi/app/secrets.json')

db = DatabaseAsync(**settings)