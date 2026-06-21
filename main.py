from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src.redis_conn import redis_pool
from src.config import Config
from src.routers import service_routers

from src.database import init_db
from src.services import CheckerService, get_checker_service

if __name__ == '__main__':

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield
        await redis_pool.disconnect()

    app = FastAPI(title="Generated image detection service", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", status_code=status.HTTP_200_OK)
    async def health_check(checker_service: CheckerService = Depends(get_checker_service)):
        return {"status": "healthy"}

    for router in service_routers:
        app.include_router(router)

    uvicorn.run(app, host=Config.HOST, port=Config.PORT)