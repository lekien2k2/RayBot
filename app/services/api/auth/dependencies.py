from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database.sqlite.models.user import User
from app.services.api.auth import service as auth_service
from app.services.api.auth.enums import RolePermission
from app.services.api.auth.exception import UnauthorizedException
from app.services.api.auth.jwt import parse_jwt_token
from app.services.api.auth.schema import JwtData
from app.services.api.dependencies import SessionDep
from app.services.api.exceptions import PermissionDeniedException
from app.services.api.user import service as user_service

RequiredAuth = Depends(parse_jwt_token)


def get_current_user(
    *, db: SessionDep = SessionDep, jwt_payload: JwtData = RequiredAuth
) -> User:
    user = user_service.get_user_by_id(db=db, user_id=jwt_payload.user_id)
    if user is None:
        raise UnauthorizedException(detail="Not authorized")

    return user


def get_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise UnauthorizedException(detail="User is not active")
    return user


def get_admin_user(user: User = Depends(get_active_user)) -> User:
    if not user.role == RolePermission.ADMIN:
        raise PermissionDeniedException()
    return user


def get_editor_user(user: User = Depends(get_active_user)) -> User:
    if not user.role in [RolePermission.ADMIN, RolePermission.EDITOR]:
        raise PermissionDeniedException()
    return user


CurrentUser = Depends(get_current_user)
CurrentActiveUserDependency = Depends(get_active_user)

RequiredEditorUserDependency = Depends(get_editor_user)
RequiredAdminUserDependency = Depends(get_admin_user)
