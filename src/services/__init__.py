import asyncio

from fastapi.params import Depends

from src.services.checker import CheckerService
from src.services.model import ModelService, ImagePreprocessedModelService


class LazyProvider[T]:

    def __init__(self, cls):
        self.cls: type[T] = cls
        self.obj: T | None = None
        self._lock = asyncio.Lock()

    async def get(self, *args, **kwargs) -> T:
        if self.obj is None:
            async with self._lock:
                if self.obj is None:
                    self.obj = self.cls(*args, **kwargs)
        return self.obj


checker_service_provider = LazyProvider[CheckerService](CheckerService)
model_service_provider = LazyProvider[ModelService](ImagePreprocessedModelService)

async def get_model_service() -> ModelService:
    return await model_service_provider.get()

async def get_checker_service(model_service: ModelService = Depends(get_model_service)) -> CheckerService:
    return await checker_service_provider.get(model_service)