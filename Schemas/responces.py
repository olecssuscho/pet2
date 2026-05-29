from pydantic import BaseModel,ConfigDict

class UserResponce(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email:str
    full_name:str

class TransactionResponceGood(BaseModel):
    model_config=ConfigDict(from_attributes=True)

    amount:float
    status:str = "Success"