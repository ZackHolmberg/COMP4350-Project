import pytest
from uuid import uuid4
from src.routes import validateSignature
from ecdsa import SigningKey, VerifyingKey
import base64

@pytest.fixture(scope='module')
def signing_key():
    return SigningKey.generate()

@pytest.fixture(scope='module')
def public_key(signing_key):
    pubk = signing_key.verifying_key.to_string()
    pubk = base64.b64encode(pubk)
    return pubk

def test_validate_signature_non_encoded(public_key):
    signature = "A Non encoded Signature"
    id_ = "Something that was signed"
    try:
        validateSignature(id_, signature, public_key)
        assert False
    except Exception as e:
        assert True

def test_validate_signature_correct(signing_key, public_key):
    id_ = str(uuid4())
    signature = signing_key.sign(id_.encode())
    signature = base64.b64encode(signature)
    
    try:
        validateSignature(id_, signature, public_key)
        assert True
    except Exception as e:
        assert False


def test_validate_signature_wrong_public_key(signing_key):
    id_ = str(uuid4())
    signature = signing_key.sign(id_.encode())
    signature = base64.b64encode(signature)
    public_key = SigningKey.generate().verifying_key.to_string()    
    try:
        validateSignature(id_, signature, public_key)
        assert False
    except Exception as e:
        assert True

def test_validate_signature_correctly_encoded_wrong_public_key(signing_key):
    id_ = str(uuid4())
    signature = signing_key.sign(id_.encode())
    signature = base64.b64encode(signature)
    public_key = base64.b64encode(SigningKey.generate().verifying_key.to_string())    
    try:
        validateSignature(id_, signature, public_key)
        assert False
    except Exception as e:
        assert True


