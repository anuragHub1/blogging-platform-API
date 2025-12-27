from fastapi import APIRouter, Depends, status,HTTPException, Query
from typing import Optional

from src.repositories.post_repository import get_all_posts, create_post, update_post, soft_delete_post, get_post_by_id
from src.utils.DBConnect import get_db
from src.schemas.common import CreatePost,UpdatePost
from src.utils.MySQLWrapper import DBConnection

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
def read_post(
    term: Optional[str] = Query(None, description="Search term"),
    db=Depends(get_db),
):
    return get_all_posts(db, term)


@router.get("/{id}")
def get_post(id:int,db:DBConnection=Depends(get_db)):
    post=get_post_by_id(db,id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post {id} not found')

    return post

@router.post("/",status_code=status.HTTP_201_CREATED)
def post_create(post:CreatePost,db:DBConnection=Depends(get_db)):
    return create_post(
        db,
        title=post.title,
        content=post.content,
        category=post.category,
        tags=post.tags,
    )

@router.put("/{id}")
def post_update(id:int,post:UpdatePost,db:DBConnection=Depends(get_db)):
    try:
        return update_post(
            db,
            post_id=id,
            title=post.title,
            content=post.content,
            category=post.category,
            tags=post.tags,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail=str(e)
        )

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:DBConnection=Depends(get_db)):
    
    deleted=soft_delete_post(db,id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post {id} not found or already deleted')
