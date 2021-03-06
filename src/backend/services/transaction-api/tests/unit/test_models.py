import pytest
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import codecs
from Crypto.Random import get_random_bytes
from src.routes import validate_signature

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
        assert False
    except Exception as e:
        assert True

def test_validate_signature_correct(public_key, signature):
    try:
        validate_signature("Test", signature, public_key)
        assert True
    except Exception as e:
        assert False

def test_validate_signature_incorrect(public_key, signature):
    try:
        validate_signature("TestIncorrect", signature, public_key)
        assert True
    except Exception as e:
        assert False

def test_validate_signature_wrong_public_key(signature):
    key = RSA.generate(bits=1024, randfunc=get_random_bytes)
    public_key = key.public_key().exportKey()
    try:
        validate_signature("Test", signature, public_key)
        assert False
    except Exception as e:
        assert True
