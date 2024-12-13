import logging

from sqlalchemy.orm.session import Session

from app.database.sqlite.models.user import User
from app.services.api.auth.exception import InvalidCredentialsException
from app.services.api.auth.schema import LoginRequest
from app.services.api.auth.utils import verify_password
from app.services.api.user.service import get_user_by_username

logger = logging.getLogger(__name__)


def authenticate_user(db: Session, *, request: LoginRequest) -> User:
    """Authenticate user with username and password."""
    logger.info(f"Authenticating user: {request.username}")
    user = get_user_by_username(db, username=request.username)
    if not user:
        logger.warning(f"User not found: {request.username}")
        raise InvalidCredentialsException()

    if not verify_password(request.password, user.password):
        logger.warning(f"Invalid credentials for user: {request.username}")
        raise InvalidCredentialsException()
    logger.info(f"User authenticated: {request.username}")
    return user


def logout(db: Session, *, username: str) -> None:
    """Logout user."""
    logger.info(f"Logging out user: {username}")
    user = get_user_by_username(db, username=username)
