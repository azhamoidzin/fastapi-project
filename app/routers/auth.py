from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import validate_email
from pydantic_core import PydanticCustomError

from app.config import settings
from app.database.session import get_db
from app.schemas.user import UserOut, UserCreate
from app.schemas.auth import Token
from app.services import user_service
from app.dependencies import auth
from app.utils.security import create_access_token, decode_access_token
from app.utils.email_send import send_activation_email


router = APIRouter(tags=["Registration and login"])


@router.post("/register", response_model=UserOut)
async def register_user(
    request: Request,
    user: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    db_user = await user_service.get_user_by_email(session, email=str(user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    token = create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=settings.activation_token_expire_minutes),
    )
    activation_link = f"{request.headers.get('host')}/activate?token={token}"
    await send_activation_email(str(user.email), activation_link)
    return await user_service.create_user(session=session, user=user)


@router.get("/activate", response_model=UserOut)
async def activate_user_by_token(token: str, session: AsyncSession = Depends(get_db)):
    token_data = decode_access_token(token)
    user = await user_service.get_user_by_email(session, str(token_data.email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.activate_user(session, str(user.email))


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db),
):
    try:
        email = validate_email(form_data.username)[1].lower()
    except (PydanticCustomError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid email address")

    user = await auth.authenticate_user(session, email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
