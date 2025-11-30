from connection_to.to_db import (
    request, delete, to_close, not_matched, new_matched,
    request_ticket, exists
    )

def get_int(prompt, minimum, maximum):
    while True:
        value = input(prompt).strip()
        try:
            value = int(value)
            if value < minimum or value > maximum:
                print("Enter a correct number")
            else:
                return value
        except ValueError:
            print("Enter a number")

def select_request_type():
    print("""
        1) Author
        2) Type
        3) Building
    """)
    return get_int("Enter number: ", 1, 3)

def handle_author():
    while True:
        name = input("Name of author: ").strip().lower()
        if exists("author", name):
            return ["author", name]
        print("Enter a valid name")

def handle_area():
    print("""
        1) Informatics
        2) Hydraulics
        3) General
    """)
    field = get_int("Enter number: ", 1, 3)
    if field == 1:
        return ["area_tag", "informatics"]
    elif field == 2:
        return ["area_tag", "hydraulics"]
    else:
        return ["area_tag", "general"]

def handle_building():
    print("""
        1) Building 1
        2) Building 2
        3) Building 3
    """)
    building = get_int("Enter number: ", 1, 3)
    return ["where_tag", f"building {building}"]

def id():
    while True:
        num = input("Enter an id: ").strip()
        if exists("external_id", num):
            return num
        print("ID not found. Try again.")


def set_priority():
    print("""
        1) Low
        2) Medium
        3) High
        4) Critical
    """)
    priority = get_int("Enter a number", 1, 4)
    if priority == 1:
        return "low"
    elif priority == 2:
        return "medium"
    elif priority == 3:
        return "high"
    else:
        return "critical"

def opeclo():
    print("""
        1) Open
        2) Close
    """)
    value = get_int("Enter a number: ", 1, 2)
    if value == 1:
        return "open"
    else:
        return "close"

def call():
    print("Select operation:")
    print("""
        1) Request type of ticket 
        2) Request ticket
        3) Close ticket
        4) Check ticket without score
        5) Set a score
        6) Delete all close ticket
        7) Exit
        """)
    score = get_int("Enter number: ", 1, 7)

    if score == 1:
        second = select_request_type()
        if second == 1:
            answer = handle_author()
        elif second == 2:
            answer = handle_area()
        else:
            answer = handle_building()
        field, value = answer
        rows = request(field, value, opeclo())
        if not rows:
            print("No tickets found.")
        else:
            for r in rows:
                print(f"[{r[0]}] ({r[7]}) {r[1]} | {r[5]} | {r[6]}")

    elif score == 2:
        answer = id()
        row = request_ticket(answer)
        if not row:
            print("No tickets found.")
        else:
            external_id, title, body, author, created_at, area_tag, where_tag, priority, status = row
            print(f"[{external_id}] ({priority}) | {status} | {title} | {area_tag} | {where_tag}")

    elif score == 3:
        answer = id()
        to_close(answer)
        print("Close selected ticket")
    
    elif score == 4:
        rows = not_matched()
        if not rows:
            print("No unmatched tickets.")
        else:
            for r in rows:
                print(f"[{r[0]}] ({r[7]}) {r[1]} | {r[5]} | {r[6]}")

    
    elif score == 5:
        new_matched(id(), set_priority())
        print("Priority updated")
    
    elif score == 6:
        delete()
        print("Deleted every close ticket")
    
    return score