from enum import Enum


class FailureReturnString(Enum):
    INCORRECT_PAYLOAD = "Please send correct json payload"
    TRANSACTION_VERFICATION_FAILURE = "Unable to Verify the Transaction"
    WALLET_VERFICATION_FAILURE = "Unable to Verify the Wallet Amount"
    UNKNOWN_FAILURE = "Something went wrong, please try again"
