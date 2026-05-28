from fastapi import FastAPI,APIRouter
from routers import Users

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(Users.router)
