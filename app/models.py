from sqlmodel import SQLModel, Field
from typing import Optional


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool = True


# схеми, які використовуємо для вхідних/вихідних даних
class ItemCreate(SQLModel):
    title: str
    description: Optional[str] = None
    price: float


class ItemRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool


class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
