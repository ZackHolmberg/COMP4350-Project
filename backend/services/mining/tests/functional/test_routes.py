import pytest
from src import app, socketio

@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


def test_home_page(test_client):
    # test GET query on '/' route
    url = '/'

    response = test_client.get(url)

    assert response.status_code == 200
    assert b"Hello From the Mining" in response.data

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