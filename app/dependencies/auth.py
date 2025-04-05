from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user_service
from app.database.session import get_db
from app.schemas.user import UserInDB
from app.utils.security import verify_password, decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def authenticate_user(session: AsyncSession, email: str, password: str):
    user = await user_service.get_user_by_email(session, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db),
) -> UserInDB:
    token_data = decode_access_token(token)
    user = await user_service.get_user_by_email(session, email=str(token_data.email))
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
