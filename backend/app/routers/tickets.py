from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.db import run_execute, run_query
from app.schemas import TicketCreate, TicketUpdate

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.get("")
def list_tickets(
    machine_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
):
    sql = """
        SELECT id, machine_id, description, status, priority, created_at, resolved_at
        FROM tickets
        WHERE (:machine_id IS NULL OR machine_id = :machine_id)
          AND (:status IS NULL OR status = :status)
        ORDER BY created_at DESC
    """
    rows = run_query(sql, {"machine_id": machine_id, "status": status})
    return {"count": len(rows), "items": rows}


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    sql = """
        SELECT id, machine_id, description, status, priority, created_at, resolved_at
        FROM tickets
        WHERE id = :ticket_id
    """
    rows = run_query(sql, {"ticket_id": ticket_id})
    if not rows:
        raise HTTPException(status_code=404, detail="工单不存在")
    return rows[0]


@router.post("", status_code=201)
def create_ticket(ticket: TicketCreate):
    machine_exists = run_query("SELECT udi FROM machines WHERE udi = :udi", {"udi": ticket.machine_id})
    if not machine_exists:
        raise HTTPException(status_code=400, detail="machine_id 对应的设备不存在")

    sql = """
        INSERT INTO tickets (machine_id, description, status, priority)
        VALUES (:machine_id, :description, :status, :priority)
        RETURNING id, machine_id, description, status, priority, created_at, resolved_at
    """
    rows = run_execute(sql, ticket.model_dump())
    return rows[0]


@router.put("/{ticket_id}")
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    existing = run_query("SELECT id, status FROM tickets WHERE id = :id", {"id": ticket_id})
    if not existing:
        raise HTTPException(status_code=404, detail="工单不存在")

    updates = ticket.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="没有提供任何更新字段")

    set_clauses = [f"{key} = :{key}" for key in updates]
    if updates.get("status") == "resolved":
        set_clauses.append("resolved_at = now()")

    sql = f"""
        UPDATE tickets SET {', '.join(set_clauses)}
        WHERE id = :id
        RETURNING id, machine_id, description, status, priority, created_at, resolved_at
    """
    updates["id"] = ticket_id
    rows = run_execute(sql, updates)
    return rows[0]


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int):
    existing = run_query("SELECT id FROM tickets WHERE id = :id", {"id": ticket_id})
    if not existing:
        raise HTTPException(status_code=404, detail="工单不存在")
    run_execute("DELETE FROM tickets WHERE id = :id", {"id": ticket_id})
