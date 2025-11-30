"""
Local server
"""
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from datetime import datetime
from pathlib import Path
import json

app = FastAPI(title="Doctor Ticket Mock API")

DATA_FILE = Path(__file__).with_name("tickets_data.json")

with DATA_FILE.open("r", encoding="utf-8") as f:
    TICKETS = json.load(f)


def parse_iso(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


"""
To load only new tickets:
I fetch the last saved ticket from the database and use its 'created_at'
as the reference time (since) for the next API request.
"""
@app.get("/tickets")
def get_tickets(
    since: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    tickets = TICKETS

    if since is not None:
        try:
            since_dt = parse_iso(since)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'since' datetime format")

        tickets = [
            t for t in tickets
            if parse_iso(t["created_at"]) > since_dt
        ]
        tickets.sort(key=lambda t: parse_iso(t["created_at"]))


    total = len(tickets)
    sliced = tickets[offset: offset + limit]

    return {
        "tickets": sliced,
        "count": len(sliced),
        "has_more": offset + limit < total,
    }


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    for t in TICKETS:
        if t["id"] == ticket_id:
            return t

    raise HTTPException(status_code=404, detail="Ticket not found")
