class LenError(BaseException):

    def __init__(self, message):
        self.message = message
