class OperationError(OSError):
    """Custom OS error to print a message"""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message
