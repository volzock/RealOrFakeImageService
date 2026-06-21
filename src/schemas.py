from datetime import datetime
from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class CheckerRunResponse(BaseModel):
    id: int
    img_hash: str
    img_name: str
    score: float
    run_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "img_hash": "abc123",
                "img_name": "image.jpg",
                "score": 95.5,
                "run_at": "2024-01-15T10:30:00+03:00"
            }
        }
    )


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Номер страницы (начиная с 1)")
    per_page: int = Field(default=20, ge=1, le=100, description="Элементов на странице")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int = Field(description="Всего записей")
    page: int = Field(description="Текущая страница")
    per_page: int = Field(description="Элементов на странице")
    pages: int = Field(description="Всего страниц")
    has_next: bool = Field(description="Есть ли следующая страница")
    has_prev: bool = Field(description="Есть ли предыдущая страница")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "per_page": 20,
                "pages": 5,
                "has_next": True,
                "has_prev": False
            }
        }
    )