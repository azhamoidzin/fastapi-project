from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database.session import create_database
from app.config import settings
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await create_database()
    print("Database initialised")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_settings.allow_origins,
    allow_credentials=settings.cors_settings.allow_credentials,
    allow_methods=settings.cors_settings.allow_methods,
    allow_headers=settings.cors_settings.allow_headers,
)

if __name__ == "__main__":
    uvicorn.run(app)
