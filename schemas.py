from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- Modelos de Eventos (Mantidos) ---

# Modelo base com os campos comuns, agora incluindo 'year'
class EventBase(BaseModel):
    image: str
    alt: str
    title: str
    date: str
    year: str
    description: str
    buttonText: str
    eventName: str
    cities: List[str] = []
    active_event: bool = True

# Modelo para a criação de um evento (herda 'year' de EventBase)
class EventCreate(EventBase):
    pass

# Modelo para atualização (todos os campos são opcionais)
class EventUpdate(BaseModel):
    image: Optional[str] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    buttonText: Optional[str] = None
    eventName: Optional[str] = None
    cities: Optional[List[str]] = None
    active_event: Optional[bool] = None

# Modelo completo do evento (herda 'year' de EventBase)
class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


# --- NOVOS Modelos de Rating ---

# Modelo para receber dados na criação de uma avaliação
class RatingCreate(BaseModel):
    # O nome do evento que está sendo avaliado (usado para referência)
    event_name: str = Field(..., description="Nome do evento avaliado, e.g., 'Linkin Park em São Paulo'")
    # O nome da pessoa que está avaliando
    reviewer_name: str = Field(..., description="Nome da pessoa que fez a avaliação")
    # A nota da avaliação, restrita entre 0 e 5
    score: int = Field(..., ge=0, le=5, description="Nota de 0 a 5")
    # Campo opcional para comentários adicionais
    comment: Optional[str] = Field(None, description="Comentários adicionais sobre a experiência")


# Modelo para o dado de avaliação retornado do banco de dados (inclui o ID e o timestamp)
class Rating(RatingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
