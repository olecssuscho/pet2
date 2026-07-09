from database import SessionLocal
from fastapi import Request
from sqlalchemy.dialects.postgresql import insert
from fastapi.responses import JSONResponse
from schemas.dbmodels import IdempotencyKeyDB,UserDB,TransactionDB
from auth import decode_token

async def idempotency_middleware(request: Request, call_next):
    db = SessionLocal()
    sendet_key = request.headers.get("X-Idempotency-Key")
    
    try:
        if sendet_key:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            payload = decode_token(token)
            user_id = None
            if payload:
                user = db.query(UserDB).filter(UserDB.email == payload.get("email")).first()
                user_id = user.id if user else None

            cached = db.query(IdempotencyKeyDB).filter(
                IdempotencyKeyDB.key == sendet_key,
                IdempotencyKeyDB.user_id == user_id
            ).first()
            
            if cached:
                transaction = db.query(TransactionDB).filter(cached.transaction_id == TransactionDB.id).first()
        
                return JSONResponse(content={"amount": transaction.amount, "status": transaction.status})

        response = await call_next(request)

        if sendet_key and response.status_code == 200:
            transaction_id = getattr(request.state, "transaction_id", None)

            stmt = insert(IdempotencyKeyDB).values(key = sendet_key, responce = response.status_code,user_id = user_id,transaction_id=transaction_id)
            stmt = stmt.on_conflict_do_nothing(index_elements=["user_id","key"])
            db.execute(stmt)
            db.commit()
        return response
    
    finally:
        db.close()