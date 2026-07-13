from fastapi import status, HTTPException, APIRouter
from sqlmodel import select
from typing import List
from .. import models, schemas, utils
from ..database import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, session: SessionDep):

    existing_user = session.exec(select(models.User).where(models.User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user with email: {user.email} already exists')


    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, session: SessionDep):
    user = session.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id: {id} was not found')

    return user