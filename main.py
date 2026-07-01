from fastapi import FastAPI
from routers import Users,Transactions,Refund,PaymentRequest,Webhook,Admin
from fastapi_pagination import add_pagination
from limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

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