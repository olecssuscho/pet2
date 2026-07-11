import time as t
from database import SessionLocal
from fastapi import Request
from schemas.dbmodels import UserDB,RequestLogDB
from auth import decode_token
from config import settings

async def request_log_middleware(request:Request, call_next):
    excluded = ["/docs", "/openapi.json", "/", "/redoc"]
    if request.url.path in excluded:
        return await call_next(request)
    
    db = SessionLocal()
    ip = request.client.host
    try:
        token = request.headers.get("Authorization","").replace("Bearer ","")
        payload = decode_token(token)
        user_id_db = None
        if payload:
            user = db.query(UserDB).filter(UserDB.email == payload.get("email")).first()
            user_id_db = user.id if user else None

        start = t.time()

        responce = await call_next(request)
        
        request.method
        time = t.time() - start
        db.add(RequestLogDB(
            user_id = user_id_db,
            process_time = time,
            method = request.method,
            status_code = responce.status_code,
            ip = ip,
            url = request.url.path
        ))
        db.commit()
        return responce
    finally:
        db.close()

