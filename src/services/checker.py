from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import CheckerRun
from src.schemas import CheckerRunResponse
from src.services.model import ModelService
from src.utils import get_hash_from_image


class CheckerService:

    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    async def score_image(self, img: Image, img_name: str, db: AsyncSession) -> CheckerRunResponse:
        img = img.resize((224, 224)).convert('RGB')
        img_hash = get_hash_from_image(img)

        score = await self.model_service.predict(img)
        run = CheckerRun(score=score, img_hash=img_hash, img_name=img_name, img_type=img.mode)
        db.add(run)
        await db.flush()
        await db.commit()
        result = CheckerRunResponse.model_validate(run)

        return result



