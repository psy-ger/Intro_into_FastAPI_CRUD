from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from app.database import get_session
from app import crud
from app.models import ItemRead, ItemCreate, ItemUpdate, Item


router = APIRouter()


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create(item: ItemCreate, session: Session = Depends(get_session)):
    created = crud.create_item(session, item)
    return created


@router.get("/", response_model=List[ItemRead])
def list_items(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return crud.get_items(session, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemRead)
def update_item_endpoint(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):
    item = crud.update_item(session, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(item_id: int, session: Session = Depends(get_session)):
    success = crud.delete_item(session, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return None