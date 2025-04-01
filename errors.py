import json

class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class JSONHandlerError(Error):
    """Exception raised for errors in the JSONHandler class.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SimpleDocumentDBError(Error):
    """Exception raised for errors in the SimpleDocumentDB class.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    

class DocumentNotFoundError(SimpleDocumentDBError):
    """Exception raised when a document is not found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


