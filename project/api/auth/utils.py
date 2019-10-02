from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token


def generate_auth_tokens(user_id):
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
