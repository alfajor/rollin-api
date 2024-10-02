import sqlite3
import secrets
from models.form import FormData

def db_connect():
    conn = None
    try:
        conn = sqlite3.connect('api.db')
        print('Success! Connected to sqlite', sqlite3.sqlite_version)
    except sqlite3.Error as err:
        print(err)
    finally:
        if conn:
            return conn
        

def generate_api_key(bits: int):
    generated_key = secrets.token_urlsafe(bits)
    return generated_key

def post_form(data: FormData):
    connection = db_connect()
    user_api_key = generate_api_key(32)
    user_token = generate_api_key(16)

    create_statement = "CREATE TABLE IF NOT EXISTS users(email TEXT UNIQUE, apiKey TEXT, userToken TEXT)"
    post_statement = "INSERT INTO users (email, apiKey, userToken) VALUES (?,?,?)"

    try: 
        with connection as conn:
            cursor = conn.cursor()

            cursor.execute(create_statement)
            cursor.execute(post_statement, [data.email, user_api_key, user_token] )
            conn.commit()
        
            # TODO: prevent duplicate email entries

    except sqlite3.Error as err:
        print(err)

    return user_api_key


# provide user supplied api key to auth endpoint 
# check for a valid key value - not currently bound to a specific user 
def check_api_key(api_key: str):
    connection = db_connect()
    try:
        with connection as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT apiKey from users WHERE apiKey = ?', [api_key])
            conn.commit()

            target_row = cursor.fetchone()
            if target_row:
                return(target_row)
            
            conn.close()
        
            return False
            
    except sqlite3.Error as err:
        print(err)
