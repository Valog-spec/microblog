import time
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from app.database.database import AsyncSessionLocal, Base, engine
from app.endpoints.api import routers

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         yield
#         await AsyncSessionLocal().close()
#         await engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    retries = 5
    while retries > 0:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                break
        except (OperationalError, asyncpg.exceptions.PostgresConnectionError) as e:
            if retries == 0:
                raise RuntimeError("Не удалось подключиться к PostgreSQL") from e
            retries -= 1
            time.sleep(5)
    yield
    await AsyncSessionLocal().close()
    await engine.dispose()


app = FastAPI(
    title="Микроблог",
    description="API для сервиса микроблогов ",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(routers)
