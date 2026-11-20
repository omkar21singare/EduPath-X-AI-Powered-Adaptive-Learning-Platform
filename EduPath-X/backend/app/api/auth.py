from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.models import User, LearnerProfile, LearningGoal
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])

SECRET_KEY = "EDUPATHX_SECRET_KEY_SUPER_SECURE_DEV_2025"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        password_hash=pwd_context.hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role or "student",
        is_demo=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = LearnerProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(profile)

    goal = LearningGoal(learner_id=profile.id, goal_name="Master Data Structures & Algorithms", target_mastery=0.85)
    db.add(goal)
    db.commit()

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token, user=user)

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token, user=user)

@router.post("/demo-login", response_model=TokenResponse)
def demo_login(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == "aarav@edupathx.edu").first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found. Please seed database.")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token, user=user)

@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        user = db.query(User).first()
    return user
