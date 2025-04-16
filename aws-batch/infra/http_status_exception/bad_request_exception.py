class BadRequestException(Exception):
    errorMessage: str = ""

    def __init__(self, errorMessage: str):
        self.errorMessage = errorMessage
    pass
