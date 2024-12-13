from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Something went wrong",
        headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestException(BaseHTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnauthorizedException(BaseHTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail,
            # headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedException(BaseHTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class NotFoundException(BaseHTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class MethodNotAllowedException(BaseHTTPException):
    def __init__(self, detail: str = "Method not allowed"):
        super().__init__(status.HTTP_405_METHOD_NOT_ALLOWED, detail)


class ConflictException(BaseHTTPException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status.HTTP_409_CONFLICT, detail)


class InvalidPasswordException(BaseHTTPException):
    def __init__(self, detail: str = "Invalid password"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)
