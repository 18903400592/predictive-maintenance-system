from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    machine_id: int
    description: str = Field(min_length=1)
    status: str = Field(default="open", pattern="^(open|in_progress|resolved|closed)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TicketUpdate(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1)
    status: Optional[str] = Field(default=None, pattern="^(open|in_progress|resolved|closed)$")
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")


class Ticket(BaseModel):
    id: int
    machine_id: int
    description: str
    status: str
    priority: str
    created_at: datetime
    resolved_at: Optional[datetime]
