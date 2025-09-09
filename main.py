from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models,schemas
app = FastAPI()


# create tables
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE - add a new user
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ - get all users
@app.get("/users/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# UPDATE - update user by id
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE - delete user by id
@app.delete("/users/{user_id}", response_model=schemas.Message)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with id {user_id} deleted"}


# CREATE expense
@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        owner_id=expense.owner_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# READ expenses
@app.get("/expenses/", response_model=list[schemas.ExpenseResponse])
def read_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

# UPDATE expense
@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db_expense.amount = expense.amount
    db_expense.description = expense.description
    db_expense.owner_id = expense.owner_id
    db.commit()
    db.refresh(db_expense)
    return db_expense

# DELETE expense
@app.delete("/expenses/{expense_id}", response_model=schemas.Message)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"message": f"Expense with id {expense_id} deleted"}

@app.get("/")
def read_root():
    return {"message": "Hello, Expense Tracker!"}
