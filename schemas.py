from pydantic import BaseModel
from typing import Optional, List 

# Modelo base com os campos comuns a todas as operações
class EventBase(BaseModel):
    image: str
    alt: str
    title: str
    date: str
    description: str
    buttonText: str
    eventName: str
    cities: List[str] = [] 
    active_event: bool = True

# Modelo para a criação de um evento (não precisa de id)
class EventCreate(EventBase):
    pass

# Modelo para atualização (todos os campos são opcionais)
class EventUpdate(BaseModel):
    image: Optional[str] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None
    buttonText: Optional[str] = None
    eventName: Optional[str] = None
    cities: Optional[List[str]] = None
    active_event: Optional[bool] = None

# Modelo completo do evento, para respostas da API (com id)
class Event(EventBase):
    id: int

    class Config:
        from_attributes = True 
