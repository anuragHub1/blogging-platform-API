from fastapi import APIRouter, Depends

from src.repositories.post_repository import get_all_posts
from src.utils.DBConnect import get_db

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/")
def read_post(db=Depends(get_db)):
    return get_all_posts(db)
