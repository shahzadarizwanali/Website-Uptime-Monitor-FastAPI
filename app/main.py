from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.api.v1.routers.websites import router as websites_router
from app.utils.scheduler import background_loop
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    task = asyncio.create_task(background_loop())
    yield
    task.cancel()
    print("Shutting down background loop")


app = FastAPI(title="Website Uptime Monitoring", lifespan=lifespan)
app.include_router(websites_router)
