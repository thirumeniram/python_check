# controller/user_controller.py
import requests
from model.database import get_connection

APP_ID = '65f190cde5c0462ad603757c'
HEADERS = {'app-id': APP_ID}

def fetch_and_store_users():
    conn = get_connection()
    cur = conn.cursor()
    response = requests.get('https://dummyapi.io/data/v1/user', headers=HEADERS)

    if response.status_code == 200:
        try:
            users = response.json()['data']
            for user in users:
                cur.execute('''
                INSERT INTO new_users (id, title, firstName, lastName, picture) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                ''', (user['id'], user['title'], user['firstName'], user['lastName'], user['picture']))
            conn.commit()
        except KeyError:
            print('The response JSON does not have the expected "data" key.')
            print(response.json())  # To see what the actual response JSON structure is
    else:
        print(f"Failed to fetch users: {response.status_code}")
        print(response.text)  # This will print the error message from the API

    cur.close()
    conn.close()

def fetch_and_store_posts():
    conn = get_connection()
    cur = conn.cursor()
    # Fetch all users' IDs from the new_users table
    cur.execute('SELECT id FROM new_users')
    user_ids = {row[0] for row in cur.fetchall()}  # Create a set of user IDs for quick lookup

    for user_id in user_ids:
        # Use the correct user ID in the request URL
        response = requests.get(f'https://dummyapi.io/data/v1/user/{user_id}/post', headers=HEADERS)
        if response.status_code == 200:
            try:
                posts = response.json()['data']
                for post in posts:
                    # Make sure the post's owner ID matches one of the user IDs in your database
                    if post['owner']['id'] in user_ids:
                        # Insert post details into new_posts, using owner.id from the post data as user_id
                        cur.execute('''
                        INSERT INTO new_posts (post_id, user_id, text, likes, publishDate) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (post_id) DO NOTHING
                        ''', (post['id'], post['owner']['id'], post['text'], post['likes'], post['publishDate']))
                conn.commit()
            except KeyError:
                print('The response JSON does not have the expected "data" key.')
                print(response.json())
        else:
            print(f"Failed to fetch posts for user {user_id}: {response.status_code}")
            print(response.json())
    cur.close()
    conn.close()


