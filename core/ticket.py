from connection_to.to_web import fetch_tickets
from connection_to.to_db import init_db, insert_ticket
from definition.scores_rules import (
    score_alert, score_problem, score_negative, score, score_critical,
)
from definition.models import (
    maintenance_area_dict, where_tuple, value_dict, negative_dict, 
    alert_dict, problem_dict,
    )

def new_body(text: str, dictionary: dict) -> str:
    text = text.lower()
    for wrong, correct in dictionary.items():
        text = text.replace(wrong, correct)
    return text

def find_alert_score(text: str, dictionary: dict) -> int:
    words = [key for key in dictionary.keys() if key in text]
    return score_alert(set(words))

def find_problem_score(text:str, dictionary:dict) -> tuple:
    words = [key for key in dictionary.keys() if key in text]
    return score_problem(words)

def find_negative_score(text:str, dictionary:dict) -> int:
    words = [key for key in dictionary.keys() if key in text]
    return score_negative(set(words))

def process_ticket(t: dict):
    title = t["title"]
    body = t["body"]
    author = t.get("author")
    building = t["where_tag"]
    created_at = t["created_at"]
    external_id = t["external_id"]

    full_body = f"{title} {body}".lower()
    full_body = new_body(full_body, value_dict)
    alert_score = find_alert_score(full_body, alert_dict)
    problem_score, problem_count = find_problem_score(full_body, problem_dict)
    negative_score = find_negative_score(full_body, negative_dict)

    total_score = score(alert_score, problem_score, negative_score)
    priority = score_critical(total_score, problem_count)

    area_tag = None
    if problem_count:
        first_problem = next(iter(problem_count.keys()))
        area_tag = maintenance_area_dict.get(first_problem)


    insert_ticket(
        external_id=external_id,
        title=title,
        body=body,
        author=author,
        created_at=created_at,
        score_tag=int(total_score),
        area_tag=area_tag,
        where_tag=building,
        priority=priority,
        problem_matched=bool(problem_count),
    )

def sync_from_web():
    init_db()
    tickets = fetch_tickets()
    for t in tickets:
        process_ticket(t)