from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Message(BaseModel):
    message: str


# Expense schemas
class ExpenseBase(BaseModel):
    amount: float
    description: str
    owner_id: int  # links to User

class ExpenseCreate(ExpenseBase):
    pass  # same as base for now

class ExpenseUpdate(ExpenseBase):
    pass  # same as base

class ExpenseResponse(ExpenseBase):
    id: int

    class Config:
        orm_mode = True