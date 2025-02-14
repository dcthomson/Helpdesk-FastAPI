from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Tickets
##########
class TicketBase(BaseModel):
    title: str
    description: str

# Schema for creating a ticket - only allows title and description
class TicketCreate(TicketBase):
    pass

# Schema for responses - includes all fields including server-generated ones
class Ticket(TicketBase):
    id: int
    created: datetime
    updated: datetime
    status: str

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Comments
###########
class CommentBase(BaseModel):
    body: str

# Schema for creating a comment - only allows body and ticket_id
class CommentCreate(CommentBase):
    ticket_id: int

# Schema for responses - includes all fields including server-generated ones
class Comment(CommentBase):
    id: int
    created: datetime
    ticket_id: int

    class Config:
        from_attributes = True

# You might also want to add a CommentUpdate schema
class CommentUpdate(BaseModel):
    body: Optional[str] = None

    class Config:
        from_attributes = True