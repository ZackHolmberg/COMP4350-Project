import pytest
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import codecs
import os, sys
from Crypto.Random import get_random_bytes
from src.routes import validate_signature, create_wallet_transaction, send_to_mine
from src.routes import get_remaining_wallet_amount, verify_receiver, retrieve_public_key

sys.path.append(os.path.abspath(os.path.join('../..', '')))
from shared import HttpCode, FailureReturnString
from shared.utils import BisonCoinUrls
from shared.exceptions import BisonCoinException, TransactionVerificationException, ReceiverException

@pytest.fixture(scope='module')
def key():
    key = RSA.generate(bits=1024, randfunc=get_random_bytes)
    return key

@pytest.fixture(scope='module')
def signing_key(key):
    private_key = key.exportKey()
    return RSA.import_key(private_key)

@pytest.fixture(scope='module')
def public_key(key):
    public_key = key.public_key().exportKey()
    return public_key.decode()

@pytest.fixture(scope='module')
def transaction_id():
    return SHA256.new(str.encode("Test"))

@pytest.fixture(scope='module')
def signature(transaction_id, signing_key):
    signer = PKCS1_v1_5.new(signing_key)
    signature = signer.sign(transaction_id)
    hexify = codecs.getencoder('hex')
    return hexify(signature)[0].decode()

def test_validate_signature_non_encoded(public_key):
    signature = "A Non encoded Signature"
    id_ = "Something that was signed"
    try:
        validate_signature(id_, signature, public_key)
        assert False #should raise an exception
    except Exception:
        assert True

def test_validate_signature_correct(public_key, signature):
    try:
        assert validate_signature("Test", signature, public_key)
    except Exception:
        assert False

def test_validate_signature_incorrect(public_key, signature):
    try:
        assert not validate_signature("TestIncorrect", signature, public_key)
    except Exception:
        assert False

def test_validate_signature_wrong_public_key(signature):
    key = RSA.generate(bits=1024, randfunc=get_random_bytes)
    public_key = key.public_key().exportKey()
    try:
        validate_signature("Test", signature, public_key)
        assert False #should raise an exception
    except Exception:
        assert True

@pytest.fixture(scope='function')
def requests_mock_transaction(requests_mock, public_key):

    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("checkWallet"),
                       json={"valid": True}, status_code=HttpCode.OK.value)

    requests_mock.get(BisonCoinUrls.user_api_url.format("umnetId/USER1"),
                       json={"success": True, "data": {"public_key": public_key}}, status_code=HttpCode.OK.value)
    
    return requests_mock

def test_create_wallet_transaction_success(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
                       json={"valid": True}, status_code=HttpCode.CREATED.value)

    try:
        create_wallet_transaction("a", "b", "c", 0000)
        assert True
    except Exception:
        assert False

def test_create_wallet_transaction_failure(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
                       json={"error": False}, status_code=HttpCode.BAD_REQUEST.value)

    try:
        create_wallet_transaction("a", "b", "c", 0000)
        assert False
    except BisonCoinException as b:
        assert "error" in b.json_message
        
def test_create_wallet_transaction_internal_server_error(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("createTransaction"),
                       json={"error": "UNKNOWN"}, status_code=HttpCode.INTERNAL_SERVER_ERROR.value)

    try:
        create_wallet_transaction("a", "b", "c", 0000)
        assert False
    except BisonCoinException as b:
        assert HttpCode.INTERNAL_SERVER_ERROR.value == b.return_code
        assert "UNKNOWN" == b.json_message["error"]

def test_send_to_mine_success(requests_mock):
    requests_mock.post(BisonCoinUrls.mining_url.format("queue"),
                       json={"success": True}, status_code=HttpCode.OK.value) 
    try:
        send_to_mine({})
        assert True
    except Exception:
        assert False

def test_send_to_mine_error(requests_mock):
    requests_mock.post(BisonCoinUrls.mining_url.format("queue"),
                       json={"error": True}, status_code=HttpCode.BAD_REQUEST.value)
    try:
        send_to_mine({})
        assert False
    except BisonCoinException as b:
        assert True
    except Exception:
        assert False

def test_get_remaining_wallet_amount(requests_mock):
    requests_mock.get(BisonCoinUrls.blockchain_wallet_url.format("balance"),
                       json={"amount": 99}, status_code=HttpCode.OK.value)

    amount = get_remaining_wallet_amount("a", "a")
    assert amount == 99


def test_verify_receiver_success(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("checkWallet"),
                       json={"valid": True}, status_code=HttpCode.OK.value) 
    try:
        verify_receiver("user")
        assert True
    except Exception:
        assert False

def test_verify_receiver_receiver_exception(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("checkWallet"),
                       json={"valid": False}, status_code=HttpCode.OK.value) 
    try:
        verify_receiver("user")
        assert False
    except ReceiverException:
        assert True
    except Exception:
        assert False

def test_verify_receiver_bisoncoin_exception(requests_mock):
    requests_mock.post(BisonCoinUrls.blockchain_wallet_url.format("checkWallet"),
                       json={"error": "UNKNOWN"}, status_code=HttpCode.BAD_REQUEST.value)
    try:
        verify_receiver("user")
        assert False
    except BisonCoinException as b:
        assert "UNKNOWN" == b.json_message["error"]
    except Exception:
        assert False

def test_send_retrieve_public_key_success(requests_mock, public_key):
    requests_mock.get(BisonCoinUrls.user_api_url.format("umnetId/USER"),
                       json={"data": { "public_key": public_key}}, status_code=HttpCode.BAD_REQUEST.value)
    try:
        key = retrieve_public_key("user")
        assert key == public_key
    except Exception:
        assert False

def test_send_retrieve_public_key_error(requests_mock):
    requests_mock.get(BisonCoinUrls.user_api_url.format("umnetId/USER"),
                       json={"error": {}}, status_code=HttpCode.BAD_REQUEST.value)
    try:
        retrieve_public_key("user")
        assert False
    except TransactionVerificationException as t:
        assert FailureReturnString.PUBLIC_KEY_NF.value in t.json_message 
    except Exception:
        assert False
