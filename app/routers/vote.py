from fastapi import status, HTTPException, APIRouter, Depends
from sqlmodel import select
from typing import List

from app import oauth2
from .. import models, schemas, utils
from ..database import SessionDep

router = APIRouter(
    prefix= "/vote",
    tags= ["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'post {vote.post_id} not found')
    
    vote_found = session.exec(select(models.Vote).where(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)).first()

    if vote.dir == 1:
        if vote_found:    
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'user {current_user.id} has already voted on the post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "succesfully added vote"}

    else:  
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f' user {current_user.id} has not voted for this post')
            
        session.delete(vote_found)
        session.commit()
        return {"message": "successfully deleted vote"}
