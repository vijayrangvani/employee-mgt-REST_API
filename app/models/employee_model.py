from sqlmodel import SQLModel,Field
from pydantic import EmailStr

class Employee(SQLModel,table=True):
    id:int | None = Field(default=None,primary_key=True)
    name:str
    email:EmailStr
    department:str
    salary:int
    is_active:bool