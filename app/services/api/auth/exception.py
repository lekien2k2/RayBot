from app.services.api.exceptions import PermissionDeniedException, UnauthorizedException


class AuthRequiredException(UnauthorizedException):
    def __init__(self):
        super().__init__("Authentication required")


class AuthorizationFailedException(PermissionDeniedException):
    def __init__(self):
        super().__init__("Authorization failed")


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Invalid credentials")


class InvalidTokenException(UnauthorizedException):
    def __init__(self):
        super().__init__("Invalid token")


class TokenExpiredException(UnauthorizedException):
    def __init__(self):
        super().__init__("Token expired")
