import time
from fastapi import Depends, status, APIRouter,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from app import db
from app import schema
auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    user_db = await db.get_user_by_email(email)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if verify_password(password, await db.get_password(email)):
        return user_db
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = int(time.time()) + 60*60*24
    to_encode.update({"expired_time": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme))->schema.UserFromDb:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id: str = payload.get("id")
        expired_time: int = payload.get("expired_time")
        if _id is None or expired_time is None or expired_time < int(time.time()):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = schema.UserFromDb(_id=_id,email=payload.get("email"))
    return user


@auth.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"id": user.id,"email":user.email})
    return {"access_token": access_token, "token_type": "Bearer"}



