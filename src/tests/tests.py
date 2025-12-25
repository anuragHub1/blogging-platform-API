from src.utils.DBConnect import connect
from src.repositories.post_repository import get_all_posts

db=connect()
post=get_all_posts(db)

print(post)

db.close_connection()