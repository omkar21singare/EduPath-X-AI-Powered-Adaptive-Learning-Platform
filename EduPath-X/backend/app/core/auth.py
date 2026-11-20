from typing import Optional, Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import User, LearnerProfile

SECRET_KEY = "EDUPATHX_SECRET_KEY_SUPER_SECURE_DEV_2025"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Resolves authenticated User from Bearer token if provided, else None."""
    if not token or not isinstance(token, str):
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            return None
        user_id = int(user_id_str)
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except (JWTError, ValueError):
        return None

def resolve_learner_id(
    explicit_learner_id: Optional[int] = None,
    current_user: Any = None,
    db: Optional[Session] = None
) -> int:
    """
    Multi-tenant resolver:
    1. If user is authenticated via JWT Bearer token and has a LearnerProfile, return that learner_id.
    2. Else if explicit_learner_id is supplied and valid (> 0), use that.
    3. Fallback to default demo learner (1).
    """
    if current_user and isinstance(current_user, User) and current_user.profile:
        return current_user.profile.id
    if explicit_learner_id and isinstance(explicit_learner_id, int) and explicit_learner_id > 0:
        return explicit_learner_id
    # Default fallback
    return 1
