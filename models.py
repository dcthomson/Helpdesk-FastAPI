from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

# Define the Database models

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now(timezone.utc))
    updated = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(String)

    comments = relationship("Comment", back_populates="ticket")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    created = Column(DateTime, default=datetime.now(timezone.utc))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))

    ticket = relationship("Ticket", back_populates="comments")