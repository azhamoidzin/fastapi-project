from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import user_service
from app.database import get_db
from app.schemas.user import UserInDB
from app.schemas.exceptions import INVALID_CREDENTIALS_401, INACTIVE_USER_400
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
        raise INVALID_CREDENTIALS_401
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise INACTIVE_USER_400
    return current_user
