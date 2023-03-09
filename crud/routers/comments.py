from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from ..database import get_db
from ..schemas import Comment_create, Comment_out
from ..models import Comment

router = APIRouter(prefix="/comment", tags=["Comments"])

@router.post("/new", response_model=Comment_out)
def create_comments(comment : Comment_create, curr_user : Session = Depends(get_current_user),
                        db : Session = Depends(get_db)):
    comment_data = comment.dict()
    new_comment = Comment(comment=comment_data["comment"], user_id=curr_user.id, post_id=comment_data["post_id"])
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment