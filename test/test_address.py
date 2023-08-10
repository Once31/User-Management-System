import unittest
import app
import server
import init_db


unittest.TestLoader.sortTestMethodsUsing = None

REGISTRATION_URL = '/api/register'
AUTH_URL = '/api/auth'
USERS_URL = '/api/users'
ADDRESSES_URL = '/addresses'

DATABASE_NAME = 'user-management-UT.db'


class AddressTest(unittest.TestCase):
    def setUp(self) -> None:
       init_db.initialize(DATABASE_NAME) #initialize database

       self.app = app.app
       self.app.testing = True

       self.app.config['DATABASE_URI'] = DATABASE_NAME
              
       self.client = self.app.test_client()

       register_user = self.client.post(REGISTRATION_URL, json ={"name" : "test user", "email": "test@gmail.com", "age": 23, "password": "test123"})
    #    print(register_user.json)
       self.new_user_id = str(register_user.json['id'])
       self.new_user_address_url = USERS_URL + "/" + self.new_user_id  + ADDRESSES_URL

       auth_resp = self.client.post(AUTH_URL, json={"email": "test@gmail.com", "password": "test123"})

       self.access_token = auth_resp.json['access_token']

       #CREATE TEST ADDRESS
       self.client.post(
           self.new_user_address_url, 
           json = {
               "address_line_1":"test",
               "city": "Nashik",
               "state": "MH",
               "pin": 422203
           },
           headers = {
               "Authorization": f"Bearer {self.access_token}"
           }
        )


    def test_get_addresses(self):
        response = self.client.get(
            self.new_user_address_url, 
            headers= {
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        self.assertEqual(response.status_code, 200)


    # def test_create_address_success(self):
    #     pass

    # def test_create_address_invalid_state_error(self):
    #     pass

    # def test_get_address_detail(self):
    #     pass

    # def test_update_address_detail(self):
    #     pass

    # def test_delete_address(self):
    #     pass
    



if __name__ == "__main__":
    unittest.main()
