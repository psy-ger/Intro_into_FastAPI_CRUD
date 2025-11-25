from sqlmodel import Session, select
from typing import List, Optional
from app.models import Item, ItemCreate, ItemUpdate


def create_item(session: Session, item_data: ItemCreate) -> Item:
    item = Item.from_orm(item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_item(session: Session, item_id: int) -> Optional[Item]:
    return session.get(Item, item_id)


def get_items(session: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    statement = select(Item).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_item(session: Session, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
    item = session.get(Item, item_id)
    if not item:
        return None
    item_data_dict = item_data.dict(exclude_unset=True)
    for key, value in item_data_dict.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, item_id: int) -> bool:
    item = session.get(Item, item_id)
    if not item:
        return False
    session.delete(item)
    session.commit()
    return True