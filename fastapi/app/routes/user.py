from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
import utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# End point /users
@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password of user
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
