# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as event_router

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API de Eventos - Anderson Viagem e Turismo",
    description="API para gerenciar os eventos de excursão.",
    version="1.0.0"
)

# Adiciona o middleware de CORS à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Inclui as rotas definidas no arquivo routes.py
app.include_router(event_router, prefix="/api/v1")

# --- Endpoints de Status ---

@app.get("/", tags=["Status"])
async def read_root():
    """ Rota principal para verificar o status da API. """
    return {"message": "Bem-vindo à API de Eventos!"}

@app.get("/health", tags=["Status"])
async def health_check():
    """
    Endpoint leve para monitoramento contínuo (health check).
    Ideal para serviços como o UptimeRobot para manter a API ativa.
    """
    return {"status": "ok", "message": "API está ativa e rodando!"}
