import requests
import jwt

class BisonCoinUrls:
    blockchain_url = "http://blockchain:5000/{:s}"
    blockchain_wallet_url = "http://blockchain:5000/wallet/{:s}"
    mining_url = "http://mining:5000/{:s}"
    user_api_url = "http://users:5000/{:s}"

def send_post_request(url, body):
    response = requests.post(url, json=body)
    return response


def send_get_request(url, body):
    response = requests.get(url, json=body)
    return response

def encode_auth_token(self, id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

def decode_auth_token(auth_token):
    payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
    return payload['sub']