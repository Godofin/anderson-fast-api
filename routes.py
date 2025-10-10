from fastapi import APIRouter, HTTPException, status
from typing import List

# Alterado de .supabase_client e .schemas para importações absolutas
from supabase_client import supabase
from schemas import Event, EventCreate, EventUpdate

router = APIRouter()
TABLE_NAME = "events"

# --- ROTA POST (CRIAÇÃO) ---
@router.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED, tags=["Events"])
async def create_event(event_data: EventCreate):
    """ Cria um novo evento no banco de dados Supabase. """
    event_dict = event_data.model_dump()
    try:
        response = supabase.table(TABLE_NAME).insert(event_dict).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail="Não foi possível criar o evento.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTAS GET (LEITURA) ---
@router.get("/events", response_model=List[Event], tags=["Events"])
async def get_active_events():
    """ Retorna todos os eventos ATIVOS do Supabase. """
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("active_event", True).order("id").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/all", response_model=List[Event], tags=["Events"])
async def get_all_events():
    """ Retorna TODOS os eventos do Supabase, ativos e inativos. """
    try:
        response = supabase.table(TABLE_NAME).select("*").order("id").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}", response_model=Event, tags=["Events"])
async def get_event_by_id(event_id: int):
    """ Retorna um evento específico pelo seu ID numérico. """
    try:
        response = supabase.table(TABLE_NAME).select("*").eq("id", event_id).single().execute()
        if not response.data:
             raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar evento: {e}")

# --- ROTA PUT (EDIÇÃO) ---
@router.put("/events/{event_id}", response_model=Event, tags=["Events"])
async def update_event(event_id: int, event_update: EventUpdate):
    """ Atualiza um evento existente no Supabase. """
    update_data = event_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    try:
        response = supabase.table(TABLE_NAME).update(update_data).eq("id", event_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Evento com id {event_id} não encontrado.")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DELETE (EXCLUSÃO) ---
@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Events"])
async def delete_event(event_id: int):
    """ Deleta um evento do Supabase. """
    try:
        supabase.table(TABLE_NAME).delete().eq("id", event_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
