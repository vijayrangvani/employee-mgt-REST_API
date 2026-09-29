from fastapi import FastAPI
from app.routers.employees import router
from app.routers.auth import auth_router
from app.database import create_table


async def lifespan(app):
    print("Application Starts..")
    create_table()
    print("creating Tables...")
    yield

app = FastAPI(title="Employee MGT API",
              lifespan=lifespan,
              version="1.0.0")

app.include_router(router,prefix="/employee")
app.include_router(auth_router,prefix="/auth")


@app.get("/") 
def root():
    return {
        "API Status":"Healthy"
    }