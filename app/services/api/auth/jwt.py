import logging
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.constants import JWT_ALG, JWT_EXP, JWT_SECRET
from app.database.sqlite.models.user import User
from app.services.api.auth.exception import (
    AuthorizationFailedException,
    InvalidTokenException,
    TokenExpiredException,
)
from app.services.api.auth.schema import JwtData

logger = logging.getLogger(__name__)
security = HTTPBearer()


def create_access_token(
    *, user: User, expires_delta: timedelta = timedelta(seconds=JWT_EXP)
) -> str:
    data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": (datetime.now() + expires_delta).timestamp(),
    }
    logger.debug(data)
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)


async def parse_jwt_token(
    header: HTTPAuthorizationCredentials = Depends(security),
) -> JwtData:
    logger.debug(f"Parsing JWT token: {header}")
    if header.credentials is None:
        raise AuthorizationFailedException()
    try:
        payload = jwt.decode(header.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        logger.debug(f"JWT payload: {payload}")
        return JwtData(**payload)
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except JWTError:
        raise InvalidTokenException()
    except Exception:
        raise AuthorizationFailedException()
