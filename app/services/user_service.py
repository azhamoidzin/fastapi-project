from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.schemas.user import UserCreate, UserOut, UserInDB
from app.dependencies.auth import get_password_hash


async def get_user(session: AsyncSession, user_id: int) -> UserOut | None:
    result = await session.execute(select(User).where(User.id == user_id))
    user: User | None = result.scalars().first()
    if user is not None:
        return UserInDB.model_validate(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> UserInDB | None:
    result = await session.execute(select(User).where(User.email == email))
    user: User | None = result.scalars().first()
    if user is not None:
        return UserInDB.model_validate(user)
    return user


async def get_users(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserOut]:
    result = await session.execute(select(User).offset(skip).limit(limit))
    return [UserOut.model_validate(user) for user in result.scalars().all()]


async def create_user(session: AsyncSession, user: UserCreate) -> UserOut:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserOut.model_validate(db_user)
