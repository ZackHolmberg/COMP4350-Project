"""module containing the custom wallet exception class"""
class WalletException(Exception):
    """The custom wallet exception class"""
    def __init__(self, message):
        self.message = message
        super().__init__()
