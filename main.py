from fastapi import FastAPI
from database import engine, Base
import routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World from FastAPI"}



