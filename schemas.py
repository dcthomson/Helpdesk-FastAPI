from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Tickets
##########
class TicketCreate(BaseModel):
    title: str
    description: str

class Ticket(TicketCreate):
    id: int
    created: datetime
    updated: datetime
    status: str

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


# Comments
###########
class CommentCreate(BaseModel):
    ticket_id: int
    body: str

class Comment(CommentCreate):
    id: int
    created: datetime

class CommentUpdate(BaseModel):
    body: Optional[str] = None