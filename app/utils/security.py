"""
JWT and security functions
"""

from datetime import datetime, timedelta, UTC

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.schemas.auth import TokenData
from app.schemas.exceptions import INVALID_CREDENTIALS_401, INVALID_TOKEN_422

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: EmailStr | None = payload.get("sub")
        if email is None:
            raise INVALID_CREDENTIALS_401
        token_data = TokenData(email=email)
    except JWTError:
        raise INVALID_TOKEN_422
    return token_data
