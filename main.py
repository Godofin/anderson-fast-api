# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Alterado para uma importação relativa. Isso pode ajudar se o main.py for executado como parte de um pacote.
from .routes import router as event_router 

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Eventos - Anderson Viagem e Turismo",
    description="API para gerenciar os eventos de excursão e avaliações (ratings).",
    version="1.0.0"
)

# Adiciona o middleware de CORS à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Inclui as rotas definidas no arquivo routes.py (incluindo eventos e ratings)
app.include_router(event_router, prefix="/api/v1")

# Rota "raiz" para verificar se a API está online
@app.get("/", tags=["Root"])
async def read_root():
    """ Rota principal para verificar o status da API. """
    return {"message": "Bem-vindo à API de Eventos e Ratings!"}
