from sqlmodel import select
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Item, ItemCreate, ItemUpdate


async def create_item(session: AsyncSession, item_data: ItemCreate) -> Item:
    item = Item.from_orm(item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def get_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    return await session.get(Item, item_id)


async def get_items(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    sort_by: str = "id",
    sort_dir: str = "asc",
    owner_id: Optional[int] = None,
) -> List[Item]:
    statement = select(Item)
    if owner_id is not None:
        statement = statement.where(Item.owner_id == owner_id)
    if q:
        statement = statement.where(Item.title.contains(q))

    # sorting
    if sort_by not in {"id", "title", "price", "owner_id"}:
        sort_by = "id"
    col = getattr(Item, sort_by)
    if sort_dir.lower() == "desc":
        col = col.desc()
    else:
        col = col.asc()
    statement = statement.order_by(col)

    statement = statement.offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_item(session: AsyncSession, item_id: int, item_data: ItemUpdate, acting_owner_id: Optional[int] = None) -> Optional[Item]:
    item = await session.get(Item, item_id)
    if not item:
        return None
    if acting_owner_id is not None and item.owner_id != acting_owner_id:
        return None
    item_data_dict = item_data.dict(exclude_unset=True)
    for key, value in item_data_dict.items():
        setattr(item, key, value)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(session: AsyncSession, item_id: int, acting_owner_id: Optional[int] = None) -> bool:
    item = await session.get(Item, item_id)
    if not item:
        return False
    if acting_owner_id is not None and item.owner_id != acting_owner_id:
        return False
    await session.delete(item)
    await session.commit()
    return True
