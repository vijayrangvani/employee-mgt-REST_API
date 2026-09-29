from fastapi import APIRouter,Depends,HTTPException,Query
from sqlmodel import Session,select,or_
from app.schemas.employee_schema import EmployeeCreate,EmployeeResponse,EmployeeUpdate
from app.models.employee_model import Employee
from app.database import get_session
from typing import Literal
import logging

router = APIRouter(prefix="/employees",tags=["employees"])
logger = logging.getLogger(__name__)

@router.get("/check")
def employees_root():
    return {
        "message":"Employee Route"
    }

@router.post("/",response_model=EmployeeResponse)
def employees_create(employee:EmployeeCreate,session:Session=Depends(get_session)):
        employee_data = employee.model_dump()
        new_employee = Employee(**employee_data)
        try:
            session.add(new_employee)
            session.commit()
            session.refresh(new_employee)
        except Exception as e:
            session.rollback()
            logging.exception("Failed to complete the execution")
            raise HTTPException(
                status_code=500,
                detail="Internal System Error"
            )
        return new_employee

@router.get("/",response_model=list[EmployeeResponse])
def get_employees(search: str | None=None,
                  offset:int=Query(default=0,ge=0),
                  limit:int=Query(default=10,le=50),
                  department:str|None = None,
                  is_active:bool|None = None,
                  sort_by:Literal["name","salary"]|None="name",
                  order:Literal["asc","desc"] = "asc",
                  session:Session = Depends(get_session)):
    statement = select(Employee)
    if search:
         statement = statement.where(or_
                                     (Employee.name.contains(search),
                                      Employee.email.contains(search)))
    if department:
        statement = statement.where(Employee.department==department)
    if is_active is not None:
        statement = statement.where(Employee.is_active==is_active)
    if sort_by:
        sort_column = getattr(Employee,sort_by)
        if order == "desc":
            sort_column = sort_column.desc()
        statement = statement.order_by(sort_column)
    result = session.exec(statement.offset(offset).limit(limit)).all()
    return result

@router.get("/{id}",response_model=EmployeeResponse)
def get_employees(id:int,session:Session = Depends(get_session)):
    result = session.exec(select(Employee).where(id == Employee.id)).first()
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"{id} not found in the records"
        )
    return result

@router.put("/{id}",response_model=EmployeeResponse)
def employee_replace(id:int,employee:EmployeeCreate,session:Session = Depends(get_session)):
    existing_employee = session.exec(select(Employee).where(Employee.id == id)).first()
    if existing_employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"{id} is not found in records"
        )
    employee_data = employee.model_dump()
    for field,value in employee_data.items():
        setattr(existing_employee,field,value)
    session.add(existing_employee)
    session.commit()
    session.refresh(existing_employee)
    return existing_employee

@router.patch("/{id}",response_model=EmployeeResponse)
def employee_update(id:int,employee:EmployeeUpdate,session:Session=Depends(get_session)):
    existing_employee = session.exec(select(Employee).where(Employee.id==id)).first()
    if existing_employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"{id} not found in records"
        )
    employee_data = employee.model_dump(exclude_unset=True)

    for field,values in employee_data.items():
        setattr(existing_employee,field,values)
    session.add(existing_employee)
    session.commit()
    session.refresh(existing_employee)
    return existing_employee

@router.delete("/{id}",status_code=204)
def employee_delete(id:int,session:Session=Depends(get_session)):
    existing_employee = session.exec(select(Employee).where(Employee.id==id)).first()
    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail=f"{id} not found in records"
        )
    session.delete(existing_employee)
    session.commit()
