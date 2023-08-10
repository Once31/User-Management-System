from app import app, restful_api
from app.api.users_api import UsersApi
from app.api.user_api import UserApi
from app.api.addresses_api import AddressesApi
from app.api.address_api import AddressApi
from app.api.auth_api import ProtectedApi, AuthApi, RegisterApi, RefreshTokernApi
from app.api.users_search_api import UsersSearchApi
from app.callbacks import jwt_callbacks

restful_api.add_resource(UsersApi, '/api/users')
restful_api.add_resource(UserApi, '/api/users/<int:id>')

restful_api.add_resource(AddressesApi, '/api/users/<int:user_id>/addresses')
restful_api.add_resource(AddressApi, '/api/addresses/<int:id>')

restful_api.add_resource(ProtectedApi, '/api/protected')
restful_api.add_resource(AuthApi, '/api/auth')
restful_api.add_resource(RegisterApi, '/api/register')
restful_api.add_resource(RefreshTokernApi, '/api/refresh')

restful_api.add_resource(UsersSearchApi, '/api/users/search')

if __name__ == "__main__":
    
    app.run()