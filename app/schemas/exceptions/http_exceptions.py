from fastapi import HTTPException


INACTIVE_USER_400 = HTTPException(
    status_code=400,
    detail="Inactive user",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_EMAIL_400 = HTTPException(status_code=400, detail="Invalid email address")

INVALID_CREDENTIALS_401 = HTTPException(
    status_code=401,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
)

USER_NOT_ACTIVE_400 = HTTPException(
    status_code=400,
    detail="Inactive user",
    headers={"WWW-Authenticate": "Bearer"},
)

ENTITY_NOT_FOUND_404 = HTTPException(status_code=404, detail="Entity not found")

ALREADY_EXIST_403 = HTTPException(status_code=403, detail="Already exist")
