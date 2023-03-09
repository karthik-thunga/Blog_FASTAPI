from .. import schemas, models
from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, select
from ..database import get_db
from ..oauth2 import get_current_user
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Posts"])

# get all post
@router.get("/", response_model=list[schemas.PostOut])
def get_all_posts(tags : Optional[str]="", 
                    db: Session = Depends(get_db), 
                    limit : int = 10, 
                    skip : int = 0, 
                    search : Optional[str] = "", 
                    curr_user : Session = Depends(get_current_user)):
    # cur.execute("SELECT * FROM posts;")
    # posts = cur.fetchall()

    subquery = (
        select(
            models.Vote.post_id, 
            func.count(models.Vote.post_id).label("Votes"))
            .group_by(models.Vote.post_id)
            .subquery()
    )
    query = (
        db.query(models.PostModel, func.coalesce(subquery.c.Votes, 0))
        .outerjoin(subquery, models.PostModel.id == subquery.c.post_id)
        .filter(
            or_(
                models.PostModel.title.ilike(f'%{search}%'),
                models.PostModel.content.ilike(f'%{search}%')
            )
        )
    )

    if tags:
        tags = tags.split(",")
        query = query.join(models.PostModel.tags).filter(models.Tag.name.in_(tags)).distinct()
    results = query.limit(limit=limit).offset(skip).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    for result in results:
        vars(result[0])["votes"] = result[1]
    results = [result[0] for result in results]
    return results

@router.get("/filter", response_model=list[schemas.PostOut])
def get_post_by_tags(tags:Optional[str]="",
                        db: Session = Depends(get_db), 
                        limit : int = 10, 
                        skip : int = 0, 
                        curr_user : Session = Depends(get_current_user)):
    query = db.query(models.PostModel)
    if tags:
        tags = tags.split(",")
        query = query.join(models.PostModel.tags).filter(models.Tag.name.in_(tags)).distinct()

    results = query.limit(limit=limit).offset(skip).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {', '.join(tags)} tags not found")
    
    return results

# get post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db)):
    # cur.execute(f"""
    # SELECT * FROM posts WHERE id = %s
    # """, (id,))
    # id_post = cur.fetchone()
    id_post =  db.query(models.PostModel, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.PostModel.id, isouter=True).group_by(
            models.PostModel.id).filter(models.PostModel.id == id).first()

    if not id_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vars(id_post[0])["votes"] = id_post[1]
    id_post = id_post[0]
    
    return id_post

# create post
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post : schemas.PostCreate, 
                    db: Session = Depends(get_db), 
                    current_user : int = Depends(get_current_user)):
    c_post = post.dict(exclude={"tags"})
    # cur.execute("""INSERT INTO posts (title, content, is_published)
    # VALUES (%s, %s, %s) RETURNING *
    # """, (c_post.get('title'), c_post.get('content'), c_post.get('is_published')))
    # new_post = cur.fetchone()
    # conn.commit()

    new_post = models.PostModel(owner_id = current_user.id, **c_post)

    # Create new tag objects and append them to post
    for tag_name in post.tags:
        existed_tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if existed_tag:
            new_post.tags.append(existed_tag)
        else:
            existed_tag = models.Tag(name=tag_name)
            db.add(existed_tag)
            new_post.tags.append(existed_tag)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post.tags)
    return new_post
        

# delete post
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, 
                db : Session = Depends(get_db), 
                current_user : int = Depends(get_current_user)):
    # cur.execute(f"""
    # DELETE FROM posts WHERE id = %s RETURNING *
    # """, (id,))
    # deleted_post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorized to perform the request")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update post
@router.put("/update/{id}", response_model=schemas.PostOut)
def update_post(id : int, post : schemas.PostCreate, db : Session = Depends(get_db), 
                                    current_user : Session = Depends(get_current_user)):
    # cur.execute("""UPDATE posts SET 
    # title = %s, content = %s, is_published=%s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.is_published, id))
    # updated_post = cur.fetchone()
    # conn.commit()

    # Check requested post exist
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # check for owner
    if current_user.id != post_query.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorized to perform the request")
    post_query.update(post.dict(exclude={"tags"}), synchronize_session=False)
    # Create new tag objects and append them to post
    updated_post = post_query.first()
    updated_post.tags.clear()
    for tag_name in post.tags:
        existed_tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if existed_tag:
            updated_post.tags.append(existed_tag)
        else:
            existed_tag = models.Tag(name=tag_name)
            db.add(existed_tag)
            updated_post.tags.append(existed_tag)
    db.commit()
    return post_query.first()