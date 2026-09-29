from pydantic import BaseModel,EmailStr
    
class EmployeeCreate(BaseModel): 
    name:str
    email:EmailStr
    department:str
    salary:int
    is_active:bool

class EmployeeResponse(BaseModel): 
    id:int
    name:str
    email:EmailStr
    department:str
    salary:int
    is_active:bool

class EmployeeUpdate(BaseModel):    
    name:str | None = None
    email:EmailStr | None = None
    department:str | None = None
    salary:int | None = None
    is_active:bool | None = None