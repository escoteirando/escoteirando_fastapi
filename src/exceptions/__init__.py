class DBConnectionException(Exception):
    def __init__(self, message: str, *args, **kwargs):
        if args or kwargs:
            super().__init__(message.format(*args, **kwargs))
        else:
            super().__init__(message)


class RepositoryException(Exception):

    def __init__(self, message: str, *args, **kwargs):
        if args or kwargs:
            super().__init__(message.format(*args, **kwargs))
        else:
            super().__init__(message)
