from fastapi import APIRouter, Depends, status,HTTPException

from src.repositories.post_repository import get_all_posts, create_post,update_post
from src.utils.DBConnect import get_db
from src.schemas.common import CreatePost,UpdatePost
from src.utils.MySQLWrapper import DBConnection

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def read_post(db:DBConnection=Depends(get_db)):
    return get_all_posts(db)

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