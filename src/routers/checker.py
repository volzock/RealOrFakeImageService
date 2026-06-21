from io import BytesIO

import redis.asyncio as redis
from PIL import UnidentifiedImageError, Image
from fastapi import APIRouter, HTTPException, UploadFile, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src import redis_conn
from src.database import paginate, CheckerRun, get_db
from src.schemas import CheckerRunResponse, PaginatedResponse
from src.services import CheckerService, get_checker_service

router = APIRouter(
    prefix="/checker",
    tags=["checker"]
)

@router.post("/", response_model=CheckerRunResponse)
async def score_image(file: UploadFile,
                      checker_service: CheckerService = Depends(get_checker_service),
                      db: AsyncSession = Depends(get_db),
                      redis_connection: redis.Redis = Depends(redis_conn.get_redis)) -> CheckerRunResponse | HTTPException:
    try:
        content = BytesIO(await file.read())
        img = Image.open(content, mode="r")
        result = await checker_service.score_image(img, file.filename, db)
        return result
    except UnidentifiedImageError:
        return HTTPException(status_code=400,
                             detail=f"cannot identify image file '{file.filename}'")

@router.get("/", response_model=PaginatedResponse[CheckerRunResponse])
async def get_checker_runs(
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=20, ge=1, le=100),
        db: AsyncSession = Depends(get_db)) -> PaginatedResponse[CheckerRunResponse] | HTTPException:
    result = await paginate(db, CheckerRun, page=page, per_page=per_page)

    if page > result["pages"] > 0:
        raise HTTPException(
            status_code=404,
            detail=f"Страница {page} не существует"
        )

    return result

