from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EventBase(BaseModel):
    image: str
    alt: str
    title: str
    date: str
    date_event: str
    year: str
    description: str
    buttonText: str
    eventName: str
    cities: List[str] = []
    active_event: bool = True

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    image: Optional[str] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    date_event: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    buttonText: Optional[str] = None
    eventName: Optional[str] = None
    cities: Optional[List[str]] = None
    active_event: Optional[bool] = None

class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    event_name: str = Field(..., description="Nome do evento avaliado, e.g., 'Linkin Park em São Paulo'")
    reviewer_name: str = Field(..., description="Nome da pessoa que fez a avaliação")
    score: int = Field(..., ge=0, le=5, description="Nota de 0 a 5")
    comment: Optional[str] = Field(None, description="Comentários adicionais sobre a experiência")


class Rating(RatingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True