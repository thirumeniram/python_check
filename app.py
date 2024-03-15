# app.py
from model.database import initialize_db
from controller.user_controller import fetch_and_store_users, fetch_and_store_posts

def main():
    initialize_db()
    print("Database initialized successfully.")
    fetch_and_store_users()
    print("User data stored successfully.")
    fetch_and_store_posts()
    print("Post data stored successfully.")

if __name__ == '__main__':
    main()
