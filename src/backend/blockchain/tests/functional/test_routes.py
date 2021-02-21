import pytest
from src import app


@pytest.fixture(scope='module')
def test_client():
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


def test_chain(test_client):
    # test GET query on '/' route
    url = '/'

    response = test_client.get(url)

    assert response.status_code == 200
    assert b"Hello Blockchain" in response.data


# def test_mine(test_client):


# def test_proof(test_client):


# def test_add_wallet(test_client):


# def test_add_amount(test_client):


# def test_subtract_amount(test_client):


# def test_get_wallet_amount(test_client):
