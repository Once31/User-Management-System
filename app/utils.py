from .database import get_db_connection, commit_and_close_db_connection
from .database.user_db import get_user_details_from_email
from .exceptions import UserExistsException

from .database.user_db import create_users

def create_admin(flask_bcrypt, user):
    conn = get_db_connection()
    existing_user = get_user_details_from_email(conn, user.email)

    if existing_user is not None:
        print(f'Admin User [{existing_user.email}] already exists. Skipping creation on startup')
        return
    user.password = flask_bcrypt.generate_password_hash(user.password, 10).decode('utf-8')
    create_users(conn, user)
    commit_and_close_db_connection(conn)
    print(f'Successfully Created Admin User [{user.email}]')