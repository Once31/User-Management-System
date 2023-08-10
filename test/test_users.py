from email import header
import os
import unittest
import app
import server
import init_db

unittest.TestLoader.sortTestMethodsUsing = None

REGISTRATION_URL = '/api/register'
AUTH_URL = '/api/auth'
USERS_URL = '/api/users'

DB_NAME = 'user-management-UT.db'

class UserTest(unittest.TestCase):
    def setUp(self):
        init_db.initialize(DB_NAME) #Initialize DB

        self.app = app.app
        self.app.testing = True

        self.app.config['DATABASE_URI'] = DB_NAME #pointing to test database

        # print(self.app.config['DATABASE_URI'])

        self.client = self.app.test_client()

        self.client.post(REGISTRATION_URL, json ={"name" : "test user", "email": "test@gmail.com", "age": 23, "password": "test123"})

        auth_resp = self.client.post(AUTH_URL, json={"email": "test@gmail.com", "password": "test123"})

        self.access_token = auth_resp.json['access_token']
        # print(self.access_token)

    def test_get_users(self):

        # print('db', self.app.config['DATABASE_URI'])
        response = self.client.get(USERS_URL, headers = {
            "Authorization": f"Bearer {self.access_token}"
        })
        print('get users', response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_user_success(self):
        response = self.client.post(
            USERS_URL,
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }, 
            json={
                "name": "once",
                "email": "once@gmail.com",
                "age": 23,
                "password": "once123"
            }
        )
        print('create success',response.status_code)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 2)

    def test_create_user_error(self):
        response = self.client.post(
            USERS_URL,
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            },
            json = {
                 "name": "test user",
                "email": "test@gmail.com",
                "age": 23,
                "password": "test123"
            }
        )
        print('create error', response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_get_user_details(self):
        response = self.client.get(f"{USERS_URL}/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual(response.status_code, 200)

    def test_update_user_details(self):
        response = self.client.put(
            f"{USERS_URL}/1", 
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            },
            json = {
                 "name": "newonce",
                "email": "once@gmail.com",
                "age": 24,
                "password": "once123"
            }
        )

        print(response.json)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_details(self):
        response = self.client.delete( USERS_URL + "/1", headers = {
            "Authorization": f"Bearer {self.access_token}"
        })

        self.assertEqual( response.status_code, 200)

if __name__ == "__main__":
    # print(__package__)
    unittest.main() 