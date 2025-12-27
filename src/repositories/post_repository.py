import types
from typing import List, Dict, Any, Optional
from src.utils.MySQLWrapper import DBConnection


def create_post(
    db: DBConnection,
    title: str,
    content: str,
    category: str,
    tags: str,
) -> Dict[str, Any]:

    tags_clean = ",".join(tag.strip() for tag in tags.split(",") if tag.strip())

    query = """
        INSERT INTO posts (title, content, category, tags)
        VALUES (%s, %s, %s, %s);
    """

    db.execute(
        query,
        (title, content, category, tags_clean),
        commit=True,
    )

    result = db.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID();")

    post=result[0]
    post["tags"] = post["tags"].split(",") if post["tags"] else []

    return post


def get_all_posts(db: DBConnection,term: Optional[str]=None):
    query = """
        SELECT *
        FROM posts
        WHERE is_deleted = FALSE
    """
    params=[]

    if term:
        query += """
        AND (
                title LIKE %s
                OR content LIKE %s
                OR category LIKE %s
            )
        """
        wildcard = f"%{term}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY created_at DESC;"

    posts = db.execute(query,tuple(params))

    for post in posts:
        if post.get("tags"):
            post["tags"] = post["tags"].split(",")
        else:
            post["tags"] = []

    return posts


def get_post_by_id(db: DBConnection, post_id: int):
    query = """
        SELECT *
        FROM posts
        WHERE id = %s AND is_deleted = FALSE;
    """
    result = db.execute(query, (post_id,))
    
    if not result:
        return None
    
    post=result[0] 

    if post.get("tags"):
        post["tags"] = post["tags"].split(",")
    else:
        post["tags"] = []

    return post


def update_post(
    db: DBConnection,
    post_id: int,
    title: str,
    content: str,
    category: str,
    tags: str,
):
    tags_str = ",".join(tag.strip() for tag in tags.split(",") if tag.strip())

    query = """
        UPDATE posts
        SET title=%s, content=%s, category=%s, tags=%s
        WHERE id=%s AND is_deleted=FALSE;
    """

    db.execute(
        query,
        (title, content, category, tags_str, post_id),
        commit=True,
    )

    return get_post_by_id(db, post_id)


def soft_delete_post(db: DBConnection, post_id: int) -> bool:
    query = """
        UPDATE posts
        SET is_deleted = 1,
            deleted_at = NOW()
        WHERE id = %s AND is_deleted = 0;
    """

    db.execute(query, (post_id,), commit=True)

    result = db.execute(
        "SELECT id FROM posts WHERE id = %s AND is_deleted = 1;",
        (post_id,),
    )

    return bool(result)
