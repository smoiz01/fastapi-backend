from fastapi import FastAPI, status, HTTPException, Response, APIRouter, Depends
from sqlmodel import func, select
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import SessionDep

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostListResponse])
def get_posts(session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    
    query = (select(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).where(models.Post.title.contains(search)).limit(limit).offset(offset))

    rows = session.exec(query).all()

    posts = [
        {
            **post.model_dump(),
            "votes": votes
        }
        for post, votes in rows
    ]

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump(), user_id= current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {
        **new_post.model_dump(), 
        "votes": 0
    }

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):

    post = session.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

    vote_count = session.exec(select(func.count()).select_from(models.Vote).where(models.Vote.post_id == id)).one()

    post_return = {
            **post.model_dump(),
            "votes": vote_count,
            "user": post.user
        }
        
    return post_return

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):

    deleted = session.get(models.Post, id)
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

    if deleted.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform the requested action")

    session.delete(deleted)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):

    updated_post = session.get(models.Post, id)

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform the requested action")
    
    updated_post.sqlmodel_update(post.dict())

    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)

    vote_count = session.exec(
        select(func.count()).select_from(models.Vote).where(models.Vote.post_id == id)
    ).one()

    return {
        **updated_post.model_dump(),
        "votes": vote_count
    }
