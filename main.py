import asyncio
import os

import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

connection_string = os.environ["DB_STRING"]


async def db_connection():
    conn = await asyncpg.connect(connection_string)
    return conn


class Item(BaseModel):
    name: str


app = FastAPI()


@app.get("/start/")
async def create_test_table():
    try:
        c = await db_connection()
        await c.execute(
            """
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50)
            );
            """
        )
        return {"message": "Table created"}
    except RuntimeError:
        print("Error on runtime")


# @app.post("/items/")
# def create_item(item: Item):
#     cursor.execute("INSERT INTO test_table (name) VALUES (:name)", [item.name])
#     connection.commit()
#     return {"message": "Item inserted", "name": item.name}


# @app.get("/items/")
# def list_items():
#     cursor.execute("SELECT id, name FROM test_table")
#     rows = cursor.fetchall()
#     return [{"id": r[0], "name": r[1]} for r in rows]
