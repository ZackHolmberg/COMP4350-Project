import pytest
from src import app, socketio
import json
from time import sleep
from src.routes import send_to_connected_clients, difficulty
from src import routes
from hashlib import sha256

@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()

@pytest.fixture(scope='module')
def json_header():

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    return headers

def test_home_page(test_client):
    # test GET query on '/' route
    url = '/'

    response = test_client.get(url)

    assert response.status_code == 200
    assert b"Hello From the Mining" in response.data

def test_queueing(test_client, json_header):
    global ongoing_proof, ongoing_transaction
    url = '/queue'
    req_data = {"id" : "test"}
    response = test_client.post(url, data=json.dumps(req_data), headers=json_header)
    assert response.status_code == 200
    assert b"success" in response.data


def test_queueing_incorrect_payload(test_client, json_header):
    url = '/queue'
    response = test_client.post(url, data=None, headers=json_header)
    assert response.status_code == 400

def test_connect(test_client):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    assert socketio_test_client.is_connected()

    socketio_test_client.disconnect()
    assert not socketio_test_client.is_connected()

def test_disconnect(test_client):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    socketio_test_client.disconnect()
    assert not socketio_test_client.is_connected()

def test_emit_events(test_client):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    socketio_test_client.emit('echo', {'a':'b'})
    received = socketio_test_client.get_received()

    assert received[0]['name'] == 'response'
    assert received[0]['args'][0]['a'] == 'b'

def test_emit_events(test_client, json_header):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    send_to_connected_clients({'id': 'test'})
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'
    assert received[0]['args'][0]['id'] == 'test'

def test_wrong_payload(test_client, json_header):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    try:
        send_to_connected_clients({'not_id': 'test'})
        assert fail
    except:
        received = socketio_test_client.get_received()
        assert received == []

def test_proof_incorrect_payload(test_client, json_header):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    socketio_test_client.emit('proof', {'id':'something'})
    received = socketio_test_client.get_received()
    assert received == []

def test_proof_correct_payload(test_client, json_header, requests_mock):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    routes.difficulty = 0
    transaction = {
        'id':'test3',
        'to' : 'test1',
        'from' : 'test2',
        'amount' : 10,
        'signature' : 'test4'
        }
    send_to_connected_clients(transaction)
    
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'
    
    requests_mock.post("http://blockchain:5000/addBlock",
                       json={"success": True}, status_code=201)

    hash_ = sha256((str(5) + "test1" + "test2" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    socketio_test_client.emit('proof', {
        "id" : "test3",
        "proof" : hash_,
        "nonce": 5,
        "minerId": "test"
    })
    
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'stopProof'
    assert received[1]['name'] == 'reward'

    routes.difficulty = 4

def test_proof_incorrect_id(test_client, json_header, requests_mock):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    transaction = {
        'id':'test3',
        'to' : 'test1',
        'from' : 'test2',
        'amount' : 10,
        'signature' : 'test4'
        }
    send_to_connected_clients(transaction)
    
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'
    
    hash_ = sha256((str(5) + "test1" + "test2" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    socketio_test_client.emit('proof', {
        "id" : "test2",
        "proof" : hash_,
        "nonce": 5,
        "minerId": "test"
    })
    
    received = socketio_test_client.get_received()
    assert received == []

def test_proof_incorrect_hash(test_client, json_header, requests_mock):
    socketio_test_client = socketio.test_client(app, flask_test_client=test_client)
    transaction = {
        'id':'test3',
        'to' : 'test1',
        'from' : 'test2',
        'amount' : 10,
        'signature' : 'test4'
        }
    send_to_connected_clients(transaction)
    
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'
    
    hash_ = sha256((str(5) + "test2" + "test2" + str(10) + "test3" + "test4").encode('utf-8')).hexdigest()
    socketio_test_client.emit('proof', {
        "id" : "test3",
        "proof" : hash_,
        "nonce": 5,
        "minerId": "test"
    })
    
    received = socketio_test_client.get_received()
    assert received == []
