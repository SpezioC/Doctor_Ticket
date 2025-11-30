from core.sqldb import call, get_int
from core.ticket import sync_from_web

def db_menu():
    while True:
        score = call()
        if score == 7:
            break

def main():
    while True:
        print("""
        MAIN MENU
        1) Update tickets from website
        2) Database operations
        3) Exit program
        """)
        choice = get_int("Enter a value: ", 1, 3)

        if choice == 1:
            sync_from_web()
            print("Every thing is fine")

        elif choice == 2:
            db_menu()   

        elif choice == 3:
            print("Bye")
            break

if __name__ == "__main__":
    main()