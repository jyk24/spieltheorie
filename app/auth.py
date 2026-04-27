"""Auth-Utilities: Passwort-Hashing, JWT-Token, User-Lookup."""
import os
from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .models import User

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-bitte-in-produktion-aendern-32chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
COOKIE_NAME = "access_token"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (JWTError, ValueError):
        return None


def get_user_from_request(request, db: Session) -> User | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    user_id = decode_token(token)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()
