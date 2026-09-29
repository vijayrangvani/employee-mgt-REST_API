from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from app.models.user_model import User
from app.database import get_session
from app.schemas.auth import UserCreate,UserResponse,UserLogin
from app.security.security import get_hashpassword,verify_password

auth_router = APIRouter(tags=["auth"])

@auth_router.post("/register",response_model=UserResponse)
def user_register(user:UserCreate,session:Session = Depends(get_session)):
    exiting_user = session.exec(select(User).where(User.username == user.username)).first()
    if exiting_user:
        raise HTTPException(
            status_code=409 ,
            detail="User already exists"
        )
    hashed_password = get_hashpassword(user.password)
    new_user = User(username=user.username,password_hash=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@auth_router.post("/login",response_model=UserResponse)
def user_login(user:UserLogin,session:Session=Depends(get_session)):
    exiting_user = session.exec(select(User).where(User.username==user.username)).first()
    if not exiting_user:
        raise HTTPException(
            status_code=404,
            detail="User not found in records"
        )
    password_check=verify_password(user.password,exiting_user.password_hash)
    if not password_check:
        raise HTTPException(
            status_code=400,
            detail="UserName or Password incorrect"
        )
    return exiting_user