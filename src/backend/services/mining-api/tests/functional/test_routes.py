import pytest
from src import app, socketio
import json
from src.routes import send_to_connected_clients, difficulty
from src import routes
from hashlib import sha256
import sys
import os
sys.path.append(os.path.abspath(os.path.join('../..', '')))
from shared.utils import BisonCoinUrls

# Module level test fixtures
VALID_NONCE = 734
VALID_AMOUNT = 3
VALID_ID = "ea269ca4907f920c60eb07bc8be34451ff6f63fef69e969be83b4d29921ff70a"
VALID_SIGNATURE = "1ff49f1e529c7a21a63bb176220457ecfc000051a56079bfbdc2b4d0a56d2a1648593c56b18b0b491207e697540fc1ee7d648f37dd3c235a4f3ceabb9ecd103533d60f6c9bc07de6236325ab992b85a25d65bc83be846b8bae2d5123818cb9cc8cd0e822b3d96fe14bfb2f75e5aa5cfa0302d3b420f5affb0c0c186663747ac0"
VALID_TIMESTAMP = 1616381251
VALID_PROOF = "0000733069633f9c7ff25d8ff0e260709f87117245d1eaa959eb193507741a5b"
add_block_url = BisonCoinUrls.blockchain_url.format("addBlock")

@pytest.fixture(scope='function')
def requests_mock_mining (requests_mock):
    requests_mock.post(add_block_url, json={"success": True}, status_code=201)
    return requests_mock

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
    req_data = {"id": "test"}
    response = test_client.post(url, data=json.dumps(req_data), headers=json_header)
    assert response.status_code == 200
    assert b"success" in response.data


def test_queueing_incorrect_payload(test_client, json_header):
    url = '/queue'
    response = test_client.post(url, data=None, headers=json_header)
    assert response.status_code == 400


def test_connect(test_client):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    assert socketio_test_client.is_connected()

    socketio_test_client.disconnect()
    assert not socketio_test_client.is_connected()


def test_disconnect(test_client):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    socketio_test_client.disconnect()
    assert not socketio_test_client.is_connected()


def test_emit_events(test_client):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    socketio_test_client.emit('echo', {'a': 'b'})
    received = socketio_test_client.get_received()

    assert received[0]['name'] == 'response'
    assert received[0]['args'][0]['a'] == 'b'


def test_emit_events(test_client, json_header):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    send_to_connected_clients({'id': 'test'})
    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'
    assert received[0]['args'][0]['id'] == 'test'


def test_wrong_payload(test_client, json_header):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    try:
        send_to_connected_clients({'not_id': 'test'})
        assert False
    except:
        received = socketio_test_client.get_received()
        assert received == []


def test_proof_incorrect_payload(test_client, json_header):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    socketio_test_client.emit('proof', {'id': 'something'})
    received = socketio_test_client.get_received()
    assert received == []


def test_proof_correct_payload(test_client, json_header, requests_mock_mining):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    transaction = {
        "from": "test2", "to": "test1", "amount": VALID_AMOUNT, "timestamp": VALID_TIMESTAMP, "id": VALID_ID, "signature": VALID_SIGNATURE}
    send_to_connected_clients(transaction)

    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'

    hash_ = sha256((str(VALID_NONCE) + str(VALID_AMOUNT) + str(VALID_TIMESTAMP) + VALID_ID +
                    VALID_SIGNATURE).encode('utf-8')).hexdigest()

    assert hash_ == VALID_PROOF
    socketio_test_client.emit('proof', {
        "id": VALID_ID,
        "proof": hash_,
        "nonce": VALID_NONCE,
        "minerId": "test"
    })

    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'stopProof'
    assert received[1]['name'] == 'reward'


def test_proof_incorrect_id(test_client, json_header, requests_mock):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    transaction = {
        'id': 'test3',
        'to': 'test1',
        'from': 'test2',
        'amount': 10,
        'signature': 'test4'
    }
    send_to_connected_clients(transaction)

    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'

    hash_ = sha256((str(5) + "test1" + "test2" + str(10) +
                    "test3" + "test4").encode('utf-8')).hexdigest()
    socketio_test_client.emit('proof', {
        "id": "test2",
        "proof": hash_,
        "nonce": 5,
        "minerId": "test"
    })

    received = socketio_test_client.get_received()
    assert received == []


def test_proof_incorrect_hash(test_client, json_header, requests_mock):
    socketio_test_client = socketio.test_client(
        app, flask_test_client=test_client)
    transaction = {
        'id': 'test3',
        'to': 'test1',
        'from': 'test2',
        'timestamp': 123,
        'amount': 10,
        'signature': 'test4'
    }
    send_to_connected_clients(transaction)

    received = socketio_test_client.get_received()
    assert received[0]['name'] == 'findProof'

    hash_ = sha256((str(5) + "test2" + "test2" + str(10) +
                    "test3" + "test4").encode('utf-8')).hexdigest()
    socketio_test_client.emit('proof', {
        "id": "test3",
        "proof": hash_,
        "nonce": 5,
        "minerId": "test"
    })

    received = socketio_test_client.get_received()
    assert received == []
