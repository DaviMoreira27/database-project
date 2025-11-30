from app.dashboard.dashboard_routes import router as dashboard_router
from app.user.user_routes import router as user_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(user_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


# @app.get("/start/")
# async def create_test_table():
#     try:
#         c = await db_connection()
#         await c.execute(
#             """
#             CREATE TABLE IF NOT EXISTS test_table (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(50)
#             );
#             """
#         )
#         return {"message": "Table created"}
#     except RuntimeError:
#         print("Error on runtime")


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
