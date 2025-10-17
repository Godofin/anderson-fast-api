# main.py

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
# Corrigido para importação ABSOLUTA para funcionar no Render
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
    allow_origins=["*"], # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Inclui as rotas definidas no arquivo routes.py
app.include_router(event_router, prefix="/api/v1")

# --- Endpoints de Status ---

# Rota "raiz" para verificar se a API está online
@app.get("/", tags=["Status"])
async def read_root():
    """ Rota principal para verificar o status da API. """
    return {"message": "Bem-vindo à API de Eventos!"}

# Endpoint de "health check" para o UptimeRobot (via GET)
@app.get("/health", tags=["Status"], summary="Health check endpoint (GET)")
async def health_check_get():
    """
    Endpoint leve para monitoramento contínuo (health check).
    Ideal para verificar no navegador se a API está rodando. Retorna um status 'ok'.
    """
    return {"status": "ok"}

# NOVO: Endpoint de "health check" para o UptimeRobot (via HEAD)
@app.head("/health", tags=["Status"], summary="Health check endpoint (HEAD)")
async def health_check_head():
    """
    Endpoint super leve para monitoramento (health check) via HEAD.
    Ideal para serviços como o UptimeRobot que usam o método HEAD por padrão.
    Não retorna corpo de resposta, apenas o status 200 OK.
    """
    return Response(status_code=200)

