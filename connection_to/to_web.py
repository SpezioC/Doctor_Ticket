import requests
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000" # Url local server

def fetch_tickets(since: datetime | None = None, limit: int = 50) -> list[dict]:
    
    params = {}
    
    if since is not None:
        since_iso = since.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        params["since"] = since_iso
    
    params["limit"] = limit

    try:
        resp = requests.get(f"{BASE_URL}/tickets", params=params, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching tickets: {e}")

    data = resp.json()
    tickets = data.get("tickets") or []
    return tickets

