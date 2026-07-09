from fastapi import FastAPI
from routers import Users,Transactions,Refund,PaymentRequest,Webhook,Admin
from fastapi_pagination import add_pagination
from limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from middleware import idempotency_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import auto_delete_row

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

scheduler = BackgroundScheduler()
scheduler.add_job(auto_delete_row,'interval',days=1)
scheduler.start()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(Users.router)
app.include_router(Transactions.router)
app.include_router(Refund.router)
app.include_router(PaymentRequest.router)
app.include_router(Webhook.router)
app.include_router(Admin.router)

add_pagination(app)

app.add_middleware(BaseHTTPMiddleware,dispatch = idempotency_middleware)

