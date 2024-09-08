class ModelError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.message = message
        self.error_code = code

    def __str__(self) -> str:
        return self.message
