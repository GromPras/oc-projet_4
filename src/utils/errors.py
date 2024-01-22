class SaveError(OSError):
    def __init__(self, message) -> None:
        self.messsage = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.messsage

class LoadError(OSError):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.message

class OperationError(OSError):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return self.message