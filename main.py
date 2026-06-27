from fastapi import FastAPI
from routers import Users,Transactions,Refund,PaymentRequest,Webhook,Admin

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(Users.router)
app.include_router(Transactions.router)
app.include_router(Refund.router)
app.include_router(PaymentRequest.router)
app.include_router(Webhook.router)
app.include_router(Admin.router)