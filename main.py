from fastapi import FastAPI
from database import Base, engine

app = FastAPI()


# create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello, Expense Tracker!"}
