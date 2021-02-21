import pytest
from src import app
import sys, os
import mongomock

sys.path.append(os.path.join('..', ''))

@pytest.fixture(scope='module')
def test_client():
    # test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()

def test_home_page(test_client):
    # test GET query on '/' route

    url = '/'

    response = test_client.get(url)

    assert response.status_code == 200
    assert b"Hello Users of bisoncoin" in response.data
