from typing import Annotated

from pydantic import BaseModel, EmailStr, ConfigDict, Field, AfterValidator


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: Annotated[EmailStr, AfterValidator(lambda email: email.lower())]
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserOut):
    is_active: bool = Field(exclude=True)
    password: str = Field(exclude=True)
