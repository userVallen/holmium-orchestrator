import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

security = HTTPBearer(auto_error=False)  # Allow requests without tokens (guests)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),  # noqa: B008
) -> uuid.UUID | None:
    """
    Optional auth dependency.
    Returns the user's UUID if a valid Supabase JWT is provided,
    otherwise returns None for anonymous guest trials.
    """

    if not credentials:
        return None

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )

        user_id_str: str = payload.get("sub")
        if not user_id_str:
            return None

        return uuid.UUID(user_id_str)
    except (JWTError, ValueError):
        return None


def get_current_user(
    user_id: uuid.UUID | None = Depends(get_current_user_optional),  # noqa: B008
) -> uuid.UUID:
    """
    Strict auth dependency.
    Raises 401 Unauthorized if the user is not authenticated.
    Use this for routes that require an active account.
    """

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
