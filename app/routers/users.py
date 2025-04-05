from fastapi import APIRouter, Depends
from pydantic import NonNegativeInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.user import UserOut
from app.services import user_service
from app.dependencies import auth


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
async def read_users(
    skip: NonNegativeInt = 0,
    limit: NonNegativeInt = 100,
    session: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(auth.get_current_user),
):
    users = await user_service.get_users(session, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=UserOut)
async def read_user_me(current_user: UserOut = Depends(auth.get_current_user)):
    return current_user
