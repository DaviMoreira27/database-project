from app.dashboard.dashboard_routes import router as dashboard_router
from app.user.user_routes import router as user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Instância principal da aplicação FastAPI
app = FastAPI()

# Configuração do middleware CORS
# Necessário para permitir que o frontend (ou outros serviços)
# acessem esta API mesmo estando em domínios diferentes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],       # Permite todos os métodos (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],       # Permite qualquer header
)

# Importa e registra as rotas dos módulos de usuário e dashboard
# Todas as rotas serão acessíveis a partir de /api
app.include_router(user_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


# ROTAS DE TESTE (COMENTADAS)

# Exemplo de rota para criação de tabela de teste no banco
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

# Exemplo de rota POST para inserir items em uma tabela de teste
# @app.post("/items/")
# def create_item(item: Item):
#     cursor.execute("INSERT INTO test_table (name) VALUES (:name)", [item.name])
#     connection.commit()
#     return {"message": "Item inserted", "name": item.name}

# Exemplo de rota GET para listar items da tabela de teste
# @app.get("/items/")
# def list_items():
#     cursor.execute("SELECT id, name FROM test_table")
#     rows = cursor.fetchall()
#     return [{"id": r[0], "name": r[1]} for r in rows]
