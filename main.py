from fastapi import FastAPI
from routers import Users,Transactions,Refund

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(Users.router)
app.include_router(Transactions.router)
app.include_router(Refund.router)