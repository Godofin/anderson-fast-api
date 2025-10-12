from fastapi import APIRouter, HTTPException, status
from typing import List

# Alterado de importações absolutas para importações relativas.
# Isso resolve o "ModuleNotFoundError" quando o projeto é executado como um pacote.
from supabase_client import supabase
from schemas import Event, EventCreate, EventUpdate, Rating, RatingCreate

router = APIRouter()
TABLE_EVENT = "events" # Renomeado para maior clareza
TABLE_RATING = "rating" # Nova constante para a tabela de avaliação

# ===============================================
# --- ROTAS DE EVENTOS (Mantidas) ---
# ===============================================

# --- ROTA POST (CRIAÇÃO DE EVENTO) ---
@router.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED, tags=["Events"])
async def create_event(event_data: EventCreate):
    """ Cria um novo evento no banco de dados Supabase. """
    event_dict = event_data.model_dump()
    try:
        response = supabase.table(TABLE_EVENT).insert(event_dict).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Não foi possível criar o evento.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTAS GET (LEITURA DE EVENTOS) ---
@router.get("/events", response_model=List[Event], tags=["Events"])
async def get_active_events():
    """ Retorna todos os eventos ATIVOS do Supabase. """
    try:
        response = supabase.table(TABLE_EVENT).select("*").eq("active_event", True).order("id").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/all", response_model=List[Event], tags=["Events"])
async def get_all_events():
    """ Retorna TODOS os eventos do Supabase, ativos e inativos. """
    try:
        response = supabase.table(TABLE_EVENT).select("*").order("id").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}", response_model=Event, tags=["Events"])
async def get_event_by_id(event_id: int):
    """ Retorna um evento específico pelo seu ID numérico. """
    try:
        response = supabase.table(TABLE_EVENT).select("*").eq("id", event_id).single().execute()
        if not response.data:
             raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar evento: {e}")

# --- ROTA PUT (EDIÇÃO DE EVENTO) ---
@router.put("/events/{event_id}", response_model=Event, tags=["Events"])
async def update_event(event_id: int, event_update: EventUpdate):
    """ Atualiza um evento existente no Supabase. """
    update_data = event_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    try:
        response = supabase.table(TABLE_EVENT).update(update_data).eq("id", event_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DELETE (EXCLUSÃO DE EVENTO) ---
@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Events"])
async def delete_event(event_id: int):
    """ Deleta um evento do Supabase. """
    try:
        supabase.table(TABLE_EVENT).delete().eq("id", event_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================================
# --- NOVAS ROTAS DE RATING ---
# ===============================================

# --- ROTA POST (CRIAÇÃO DE RATING) ---
@router.post("/ratings", response_model=Rating, status_code=status.HTTP_201_CREATED, tags=["Ratings"])
async def create_rating(rating_data: RatingCreate):
    """ Cadastra uma nova avaliação (rating) para um evento. """
    # Verifica se a nota está no intervalo de 0 a 5 (já garantido pelo Pydantic, mas como segurança)
    if not 0 <= rating_data.score <= 5:
        raise HTTPException(status_code=400, detail="A nota deve ser um valor inteiro entre 0 e 5.")

    rating_dict = rating_data.model_dump()
    try:
        # Insere a avaliação na nova tabela 'rating'
        response = supabase.table(TABLE_RATING).insert(rating_dict).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Não foi possível cadastrar a avaliação.")
        return response.data[0]
    except Exception as e:
        # Pode ocorrer um erro se a tabela 'rating' não existir no Supabase
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar avaliação. Verifique se a tabela '{TABLE_RATING}' existe: {str(e)}")


# --- ROTA GET (LEITURA DE TODOS OS RATINGS) ---
@router.get("/ratings", response_model=List[Rating], tags=["Ratings"])
async def get_all_ratings():
    """ Retorna todas as avaliações cadastradas. """
    try:
        # Busca todas as avaliações na tabela 'rating'
        response = supabase.table(TABLE_RATING).select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- ROTA GET (LEITURA DE RATINGS POR EVENTO) ---
@router.get("/ratings/event/{event_name}", response_model=List[Rating], tags=["Ratings"])
async def get_ratings_by_event(event_name: str):
    """ Retorna todas as avaliações para um evento específico (filtrando por event_name). """
    try:
        # Filtra as avaliações pelo nome do evento
        response = supabase.table(TABLE_RATING).select("*").eq("event_name", event_name).order("created_at", desc=True).execute()

        if not response.data:
            # Não é um erro 404 se a lista estiver vazia, mas sim um retorno de lista vazia
            return []

        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar avaliações para o evento '{event_name}': {str(e)}")
