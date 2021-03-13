from .httpcodes import HttpCode
from .returnstrings import FailureReturnString


class BisonCoinException(Exception):
    client_error = HttpCode.BAD_REQUEST.value

    def __init__(self, json_message=FailureReturnString.UNKNOWN_FAILURE.value, return_code=HttpCode.INTERNAL_SERVER_ERROR.value):
        self.json_message = json_message
        self.return_code = return_code
        super(Exception, self).__init__()


class IncorrectPayloadException(BisonCoinException):
    def __init__(self):
        super(BisonCoinException, self).__init__(
            FailureReturnString.INCORRECT_PAYLOAD.value, HttpCode.BAD_REQUEST.value)


class TransactionVerificationException(BisonCoinException):
    def __init__(self, json_message=FailureReturnString.SIGNATURE_VERFICATION_FAILURE.value, return_code=HttpCode.BAD_REQUEST.value):
        super(BisonCoinException, self).__init__(json_message, return_code)


class ReceiverException(BisonCoinException):
    def __init__(self):
        super(BisonCoinException, self).__init__(FailureReturnString.RECEIVER_NOT_PRESENT.value,
                                                 HttpCode.BAD_REQUEST.value)


class UserNotFoundException(BisonCoinException):
    def __init__(self):
        super(BisonCoinException, self).__init__(
            FailureReturnString.USER_NOT_FOUND.value, HttpCode.BAD_REQUEST.value)


class DatabaseVerificationException(BisonCoinException):
    def __init__(self, error_messsage="Unknown Error"):
        self.error_message = error_messsage
        super(BisonCoinException, self).__init__(FailureReturnString.DATABASE_VERIFICATION_FAILURE.value,
                                                 HttpCode.BAD_REQUEST.value)


class IncorrectCredentialsException(BisonCoinException):
    def __init__(self):
        super(BisonCoinException, self).__init__(FailureReturnString.INCORRECT_CREDENTIALS.value,
                                                 HttpCode.BAD_REQUEST.value)
