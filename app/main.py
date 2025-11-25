from fastapi import FastAPI
from app.routers import items
from app.database import init_db

app = FastAPI(title="FastAPI CRUD Demo")

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI CRUD"}


@app.on_event("startup")
def on_startup():
    init_db()
