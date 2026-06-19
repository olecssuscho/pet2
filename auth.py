from datetime import timedelta,timezone,datetime
from jose import jwt,JWTError
from passlib.context import CryptContext
from config import settings
contex = CryptContext(schemes=["argon2","bcrypt"], deprecated="auto")

def hash_password(password:str):
    return contex.hash(password)

def verify_password(password:str, password_to_check:str):
    return contex.verify(password,password_to_check)

def create_access_token(data:dict):
    to_encode = data.copy()
    to_encode.update({"type":"access"})
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET,settings.ALGORITHM)

def create_refresh_token(data:dict):
    to_encode = data.copy()
    to_encode.update({"type":"refresh"})
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET,settings.ALGORITHM)

def decode_token(token:str):
    try:
        payload = jwt.decode(token,settings.SECRET,[settings.ALGORITHM])
        return payload
    except JWTError:
        return None