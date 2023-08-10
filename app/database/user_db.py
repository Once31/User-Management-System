from app.exceptions import UserNotFountException
from ..models.user import User

def get_users(conn):
   results =  conn.execute('SELECT * FROM user').fetchall()
   results = [dict(row) for row in results]
   return results

def create_users(conn, user):
   conn.execute('INSERT INTO user (name, email, age, password, role) values (?,?,?,?,?)',(user.name, user.email, user.age, user.password, user.role))
   return get_user_details_from_email(conn, user.email)


def get_user(conn, id):
   result = conn.execute('SELECT * FROM user WHERE id = ?',(str(id))).fetchone()
   if result is None:
      raise UserNotFountException(f'user with [id : {id}] not found in DATABASE.', 400)
   
   return dict(result) if result != None else None

def update_user(conn, id, user):
   print('user', user.name)
   conn.execute('UPDATE user SET name = ?, email = ?, age = ?, password = ?, role = ? where id = ?', (user.name, user.email, user.age, user.password,user.role, str(id)))

def delete_user(conn, id):
   conn.execute('DELETE FROM user WHERE id = ?', (str(id)))

def get_user_details_from_email(conn, email):
   result = conn.execute('select * from user where email = ?',(email,)).fetchone()
   return User.from_json(dict(result)) if result is not None else None

def delete_users(conn):
   conn.execute('delete from user')

