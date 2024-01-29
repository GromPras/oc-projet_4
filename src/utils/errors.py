class SaveError(OSError):
    """Custom error class"""
    def __init__(self, message) -> None:
        self.messsage = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.messsage

class LoadError(OSError):
    """Custom error class"""
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.message

class OperationError(OSError):
    """Custom error class"""
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.message