from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models

router = APIRouter(prefix="/votes", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(votes : schemas.Vote, db : Session = Depends(get_db), 
            current_user : Session = Depends(get_current_user)):
    
    if not db.query(models.PostModel).filter(models.PostModel.id == votes.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Post {votes.post_id} not found")
    
    votes_query = db.query(models.Vote).filter(
        models.Vote.post_id == votes.post_id,
        models.Vote.user_id == current_user.id
    )

    # For adding vote
    if votes.dir == 1:
        if votes_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} already voted for post {votes.post_id}")
        # add entry to votes
        new_vote = models.Vote(user_id=current_user.id, post_id=votes.post_id)
        db.add(new_vote)
        db.commit()
        return {
            "message" : f"User {current_user.id} voted for post {votes.post_id}"
        }
    # For removing vote
    if votes.dir == 0:
        if not votes_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail=f"User {current_user.id} not voted for post {votes.post_id}")
        # remove entry from votes
        votes_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message" : f"User {current_user.id} vote deleted for post {votes.post_id}"
        }
    # Invalid direction for vote
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Invalid direction for vote")

