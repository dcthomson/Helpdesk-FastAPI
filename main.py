from fastapi import FastAPI, Depends, status, HTTPException
import schemas
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, timezone

app = FastAPI()

models.Base.metadata.create_all(bind=engine)        # Create the tables in the database

def get_db():       # Dependency to get the database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Ticket
@app.post("/ticket", status_code=status.HTTP_201_CREATED, tags=["tickets"])
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    new_ticket = models.Ticket(title=ticket.title, description=ticket.description, status='open')
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

# Get all tickets
@app.get('/tickets', status_code=status.HTTP_200_OK, tags=["tickets"])
def all(db: Session = Depends(get_db)):
    tickets_query = db.query(models.Ticket).all()
    return tickets_query

# Get ticket by id
@app.get('/ticket/{ticket_id}', status_code=status.HTTP_200_OK, tags=["tickets"])
def show(ticket_id: int, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket {ticket_id} not found")
    return ticket_query

# Update ticket
@app.put('/ticket/{ticket_id}', status_code=status.HTTP_202_ACCEPTED, tags=["tickets"])
def update(ticket_id: int, ticket: schemas.TicketUpdate, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == ticket_id)
    existing_query = ticket_query.first()
    if not existing_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket {ticket_id} not found")
    update_data = ticket.model_dump(exclude_unset=True)
    update_data["updated"] = datetime.now(timezone.utc)
    ticket_query.update(update_data)
    db.commit()
    db.refresh(existing_query)
    return existing_query

# Delete Ticket
@app.delete('/ticket/{ticket_id}', status_code=status.HTTP_200_OK, tags=["tickets"])
def destroy(ticket_id: int, db: Session = Depends(get_db)):
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket {ticket_id} not found")
    db.delete(ticket_query)
    db.commit()
    return f"ticket {ticket_id} deleted"

# Create Comment
@app.post('/comment', status_code=status.HTTP_201_CREATED, tags=["comments"])
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    # check if ticket exists first:
    ticket_query = db.query(models.Ticket).filter(models.Ticket.id == comment.ticket_id).first()
    if not ticket_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket {comment.ticket_id} not found")
    new_comment = models.Comment(ticket_id=comment.ticket_id, body=comment.body)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# get comments by ticket id
@app.get('/comments-by-ticket-id/{ticket_id}', status_code=status.HTTP_200_OK, tags=["comments"])
def show_comments(ticket_id: int, db: Session = Depends(get_db)):
    comments_query = db.query(models.Comment).filter(models.Comment.ticket_id == ticket_id).all()
    if not comments_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comments for ticket {ticket_id} not found")
    return comments_query

# Get comment by id
@app.get('/comment/{comment_id}', status_code=status.HTTP_200_OK, tags=["comments"])
def show_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")
    return comment_query

# Update comment
@app.put('/comment/{comment_id}', status_code=status.HTTP_202_ACCEPTED, tags=["comments"])
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    existing_comment = comment_query.first()
    if not existing_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")
    update_data = comment.model_dump(exclude_unset=True)
    comment_query.update(update_data)
    db.commit()
    db.refresh(existing_comment)
    return existing_comment

# Delete comment
@app.delete('/comment/{comment_id}', status_code=status.HTTP_200_OK, tags=["comments"])
def destroy_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {comment_id} not found")
    db.delete(comment_query)
    db.commit()
    return f"comment {comment_id} deleted"