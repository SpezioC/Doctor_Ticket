import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "doctor_ticket.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    create_sql = """
    CREATE TABLE IF NOT EXISTS tickets (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        external_id     TEXT NOT NULL,        -- ID ticket web
        title           TEXT NOT NULL,        
        body            TEXT NOT NULL,        
        author          TEXT,                 
        created_at      TEXT NOT NULL,
        score_tag       INTEGER,                       
        area_tag        TEXT,
        where_tag       TEXT,                 
        priority        TEXT NOT NULL,        
        problem_matched INTEGER NOT NULL,     
        inserted_at     TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        status          TEXT,
        UNIQUE(external_id)
    );

    """
    with get_connection() as conn:
        conn.execute(create_sql)


def insert_ticket(
    external_id: str,
    title: str,
    body: str,
    author: str | None,
    created_at: str,
    score_tag: int,
    area_tag: str | None,
    where_tag: str | None,
    priority: str,
    problem_matched: bool,
) -> None:
    
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO tickets (
                external_id, title, body, author, created_at,
                score_tag, area_tag, where_tag, priority,
                problem_matched, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open');
            """,
            (
                external_id,
                title,
                body,
                author,
                created_at,
                score_tag,
                area_tag,
                where_tag,
                priority,
                1 if problem_matched else 0,
            ),
        )

# Request by type
def request(field: str, value: str, status: str):
    query = f"""
        SELECT external_id, title, body, author, created_at,
               area_tag, where_tag, priority
        FROM tickets
        WHERE status = ? AND {field} = ?
        ORDER BY score_tag DESC;
    """

    with get_connection() as conn:
        cur = conn.execute(query, (status, value))
        rows = cur.fetchall()
    return rows

# Delete every close ticket
def delete():
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM tickets WHERE status = 'close';
            """
            )

# Set close a ticket
def to_close(external_id: str):
    query = """
        UPDATE tickets SET status = 'close'
        WHERE external_id = ?
    """
    with get_connection() as conn:
        cur = conn.execute(query, (external_id,))
        if cur.rowcount == 0:
            print("ID not found")

# Problem without score
def not_matched():
    with get_connection() as conn:
        cur = conn.execute(
            """
            SELECT external_id, title, body, author, created_at,
                   area_tag, where_tag, priority
            FROM tickets
            WHERE problem_matched = 0;
            """
        )
        rows = cur.fetchall()
    return rows

# Set new value for ticket
def new_matched(external_id: str, priority: str):
    query = """
        UPDATE tickets
        SET priority = ?, problem_matched = 1
        WHERE external_id = ?
    """
    with get_connection() as conn:
        cur = conn.execute(query, (priority, external_id))
        if cur.rowcount == 0:
            print("ID not found")

# Request ticket
def request_ticket(external_id: str):
    query = """
        SELECT external_id, title, body, author, created_at,
               area_tag, where_tag, priority, status
        FROM tickets
        WHERE external_id = ?
    """
    with get_connection() as conn:
        cur = conn.execute(query, (external_id,))
        row = cur.fetchone()
    
    return row

# Check if exist
def exists(field: str, value: str) -> bool:
    query = f"""
        SELECT EXISTS(
            SELECT 1 FROM tickets WHERE {field} = ?
        );
    """
    with get_connection() as conn:
        cur = conn.execute(query, (value,))
        (exists,) = cur.fetchone()
        return bool(exists)