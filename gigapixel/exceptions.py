class GigapixelException(Exception):
    pass


class NotFile(GigapixelException):
    pass


class FileAlreadyExists(GigapixelException):
    pass


class ElementNotFound(GigapixelException):
    pass
