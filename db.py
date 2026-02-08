import asyncio
import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
app = FastAPI()

class UserData(BaseModel):
    id: int
    username: str
    email: str

@app.on_event("startup")
async def startup():
    app.state.db_conn = await asyncpg.create_pool(
                host="192.168.1.252",
                port=5544,
                user="postgres",
                password="admin",
                database="TestDB"
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_conn.close()

@app.get("/get_all_users", response_model=List[UserData])
async def get_all_users():
    async with app.state.db_conn.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM table01")
        return [dict(r) for r in rows]

@app.get("/one_user{item_id}")
async def one_user(item_id:int):
    async with app.state.db_conn.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM table01")
        for user in rows:
            user_item = dict(user)
            if user_item["id"] == item_id:
                return user_item

@app.get("/one_item{item_id}")
async def one_item(item_id:int):
    async with app.state.db_conn.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM table01 WHERE id=$1",
                                  item_id)
        return user

