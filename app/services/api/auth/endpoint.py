from fastapi import APIRouter, status

from app.services.api.auth import service as auth_service
from app.services.api.auth.dependencies import RequiredAuth
from app.services.api.auth.jwt import create_access_token
from app.services.api.auth.schema import LoginRequest, LoginResponse
from app.services.api.dependencies import SessionDep

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTcxMTEyMTI0Mi4xNDkwNn0.SbwgbaUG6fBbAW2yWddl72OfdqnvlnuxpCNwlCqPXro"
                    }
                }
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {"example": {"detail": "Invalid credentials"}}
            },
        },
    },
)
def login(db: SessionDep, *, request: LoginRequest):
    user = auth_service.authenticate_user(db, request=request)
    return LoginResponse(access_token=create_access_token(user=user), role=user.role)


@router.post(
    "/logout",
    dependencies=[RequiredAuth],
    status_code=status.HTTP_204_NO_CONTENT,
    responses={204: {"description": "Logout successful"}},
)
def logout(db: SessionDep, *, username: str):
    auth_service.logout(db, username=username)
