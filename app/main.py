
from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(
    title="IT Navigator",
    description="AI-powered IT HelpDesk system",
    version="0.2.0"
)


# Допустимые статусы заявки
TicketStatus = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed"
]


# Модель входящих данных при создании заявки
class TicketCreate(BaseModel):
    title: str
    description: str
    category: str


# Модель данных для изменения статуса
class TicketUpdate(BaseModel):
    status: TicketStatus


# Временное хранилище заявок
tickets = {}

# Счётчик ID
next_ticket_id = 1


# Проверка работоспособности сервера
@app.get("/")
def root():
    return {
        "message": "Welcome to IT Navigator!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# CREATE: создание заявки
@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_data: TicketCreate):
    global next_ticket_id

    ticket = {
        "id": next_ticket_id,
        "title": ticket_data.title,
        "description": ticket_data.description,
        "category": ticket_data.category,
        "status": "open"
    }

    tickets[next_ticket_id] = ticket
    next_ticket_id += 1

    return {
        "message": "Ticket created successfully",
        "ticket": ticket
    }


# READ: получение всех заявок
@app.get("/tickets")
def get_tickets():
    return {
        "total": len(tickets),
        "tickets": list(tickets.values())
    }


# READ: получение одной заявки
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    ticket = tickets.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# UPDATE: изменение статуса заявки
@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket_data: TicketUpdate):
    ticket = tickets.get(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    ticket["status"] = ticket_data.status

    return {
        "message": "Ticket updated successfully",
        "ticket": ticket
    }


# DELETE: удаление заявки
@app.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    if ticket_id not in tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    del tickets[ticket_id]

    return None
