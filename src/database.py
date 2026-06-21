import logging
from contextlib import asynccontextmanager
from datetime import datetime
from math import ceil
from typing import AsyncGenerator
from zoneinfo import ZoneInfo

from sqlalchemy import Integer, String, Float, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

from src.config import Config

logger = logging.getLogger(__name__)

database_url = Config.DATABASE_URL
logger.info("Initializing database with url: {}".format(database_url))
print(database_url)
Base = declarative_base()
engine = create_async_engine(
    database_url,
    echo=True,
    pool_size=20,
    max_overflow=30,
    pool_recycle=3600,
)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


class CheckerRun(Base):
    __tablename__ = 'checker_runs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    img_hash: Mapped[str] = mapped_column(String, nullable=False)
    img_name: Mapped[str] = mapped_column(String, nullable=False)
    img_type: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)

    run_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(ZoneInfo('Europe/Moscow'))
    )

    def __repr__(self) -> str:
        return (
            f"<CheckerRun(id={self.id}, "
            f"img_hash='{self.img_hash}', "
            f"img_name='{self.img_name}', "
            f"img_type='{self.img_type}', "
            f"score={self.score}, "
            f"run_at='{self.run_at}')>"
        )



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def paginate(
        db: AsyncSession,
        model,
        page: int = 1,
        per_page: int = 20,
        filters=None
) -> dict:
    query = select(model)

    if filters:
        query = query.filter(*filters) if hasattr(query, 'filter') else query.where(*filters)

    count_query = select(func.count(model.id)).select_from(model)
    if filters:
        count_query = count_query.where(*filters)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    paginated_query = (
        query
        .order_by(model.id.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    result = await db.execute(paginated_query)
    items = result.scalars().all()

    pages = ceil(total / per_page) if total > 0 else 0

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
    }


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()