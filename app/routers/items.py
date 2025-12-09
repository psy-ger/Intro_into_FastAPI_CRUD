from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app import crud
from app.models import ItemRead, ItemCreate, ItemUpdate


router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    created = await crud.create_item(session, item)
    return created


@router.get("/", response_model=List[ItemRead])
async def list_items(
    skip: int = 0,
    limit: int = 10,
    q: Optional[str] = Query(None, description="Search in title"),
    sort_by: str = Query("id", description="Sort by: id,title,price,owner_id"),
    sort_dir: str = Query("asc", description="Sort direction: asc or desc"),
    owner_id: Optional[int] = Query(None, description="Filter by owner id"),
    session: AsyncSession = Depends(get_session),
):
    items = await crud.get_items(
        session, skip=skip, limit=limit, q=q, sort_by=sort_by, sort_dir=sort_dir, owner_id=owner_id
    )
    return items


@router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item_endpoint(
    item_id: int,
    item_update: ItemUpdate,
    owner_id: Optional[int] = Query(
        None, description="Acting owner id for authorization"),
    session: AsyncSession = Depends(get_session),
):
    item = await crud.update_item(session, item_id, item_update, acting_owner_id=owner_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="Item not found or not permitted")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_endpoint(
    item_id: int,
    owner_id: Optional[int] = Query(
        None, description="Acting owner id for authorization"),
    session: AsyncSession = Depends(get_session),
):
    success = await crud.delete_item(session, item_id, acting_owner_id=owner_id)
    if not success:
        raise HTTPException(
            status_code=404, detail="Item not found or not permitted")
    return None
