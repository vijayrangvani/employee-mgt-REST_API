from dotenv import load_dotenv
import os
from sqlmodel import Session,create_engine,SQLModel
from app.models.employee_model import Employee

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
def create_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session