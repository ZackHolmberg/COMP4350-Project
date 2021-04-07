import requests


class BisonCoinUrls:
    blockchain_url = "http://api-gateway/blockchain/{:s}"
    blockchain_wallet_url = "http://api-gateway/blockchain/wallet/{:s}"
    mining_url = "http://mining:5000/{:s}"
    user_api_url = "http://users:5000/{:s}"

def send_post_request(url, body):
    response = requests.post(url, json=body)
    return response


def send_get_request(url, body):
    response = requests.get(url, json=body)
    return response
    
