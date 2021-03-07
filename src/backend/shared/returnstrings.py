from enum import Enum


class FailureReturnString(Enum):
    INCORRECT_PAYLOAD = "Please send correct json payload"
    TRANSACTION_VERFICATION_FAILURE = "Unable to Verify the Transaction"
    WALLET_VERFICATION_FAILURE = "Unable to Verify the Wallet Amount"
    UNKNOWN_FAILURE = "Something went wrong, please try again"
    RECEIVER_NOT_PRESENT = "The receiver you are trying to send the money to doesn't exist"
    DATABASE_VERIFICATION_FAILURE = "Database validation failed! Please check your input and try again."
    SIGNATURE_VERFICATION_FAILURE = "signature verification failed"
    USER_NOT_FOUND = "user not found in the database"
    TRANSACTION_CREATION_FAILURE = "Unable to create a transaction"