from pydantic import BaseModel

class User(BaseModel):
    email:str
    password:str
    full_name:str
    balance:float
    is_blocked:bool
    created_at:str