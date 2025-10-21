from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.api.v1.routers.websites import router as websites_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    yield
    print("shutting down")


app = FastAPI(title="Website Uptime Monitoring", lifespan=lifespan)

app.include_router(websites_router)
