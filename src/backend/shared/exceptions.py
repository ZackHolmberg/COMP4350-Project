from .httpcodes import HttpCode
from .returnstrings import FailureReturnString

class BisonCoinException(Exception):
    client_error = HttpCode.BAD_REQUEST.value
    def __init__(self, json_message=FailureReturnString.UNKNOWN_FAILURE.value, return_code=HttpCode.INTERNAL_SERVER_ERROR.value):
        self.json_message = json_message
        self.return_code = return_code
        super().__init__()

class IncorrectPayloadException(BisonCoinException):
    def __init__(self):
        super().__init__(json_message=FailureReturnString.INCORRECT_PAYLOAD.value, return_code=HttpCode.BAD_REQUEST.value)

class TransactionVerificationException(BisonCoinException):
    def __init__(self, json_message=FailureReturnString.SIGNATURE_VERFICATION_FAILURE.value, return_code= HttpCode.BAD_REQUEST.value):
        super().__init__(json_message=json_message, return_code=return_code)

class WalletVerificationException(BisonCoinException):
    def __init__(self):
        super().__init__(json_message=FailureReturnString.WALLET_VERFICATION_FAILURE.value, return_code=HttpCode.BAD_REQUEST.value)

class ReceiverException(BisonCoinException):
    def __init__(self):
        super().__init__(json_message=FailureReturnString.RECEIVER_NOT_PRESENT.value, return_code=HttpCode.BAD_REQUEST.value)
