from src.routes import authenticate_user
import sys
import os
sys.path.append(os.path.abspath(os.path.join('../..', '')))

from shared.exceptions import BisonCoinException
from shared.utils import BisonCoinUrls

auth_url = BisonCoinUrls.user_api_url.format("authUser")

def test_authenticate_user_success(requests_mock):
    requests_mock.post(auth_url, json={"success": True})
    try:
        authenticate_user("u", "p")
        assert True
    except Exception:
        assert False

def test_authenticate_user_failure(requests_mock):
    requests_mock.post(auth_url, json={"success": False})
    try:
        authenticate_user("u", "p")
        assert False
    except Exception as e:
        assert type(e) == BisonCoinException

def test_authenticate_user_exception(requests_mock):
    requests_mock.post(auth_url, json={"error": "AUTH FAILURE"})
    try:
        authenticate_user("u", "p")
        assert False
    except BisonCoinException as b:
        assert "AUTH FAILURE" in b.json_message["error"]
    except Exception:
        assert False 
