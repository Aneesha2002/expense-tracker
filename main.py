from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models

app = FastAPI()


# create tables
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#CREATE - add a new user
@app.post("/users/")
def create_user(username: str, password: str, db:Session = Depends(get_db)):
    user = models.User(username=username,password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#READ - get all users
@app.get("/users/")
def read_users(db: Session= Depends(get_db)):
    users = db.query(models.User).all()
    return users

#UPDATE - update user by id
@app.put("/users/{user_id}")
def update_user(user_id: int, username: str, password: str, db: Session =Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User nt found")
    user.username = username
    user.password = password
    db.commit()
    db.refresh(user)
    return user

#DELETE - delete user by id
@app.delete("/users/{user_id}")
def delete_user(user_id:int,db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found ")
    db.delete(user)
    db.commit()
    return {"message": f"User with id {user_id} deleted"}

@app.get("/")
def read_root():
    return {"message": "Hello, Expense Tracker!"}
