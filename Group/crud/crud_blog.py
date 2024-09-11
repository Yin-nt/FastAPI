from sqlalchemy import Session
from Group import models, schemas

def creat_blog(db: Session, blog: schemas.CreatBlog):
    db_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        group_id=blog.group_id,
        author_id=blog.author_id,
        permission=blog.permission,
        creat_at=blog.creat_at,
        updated_at=blog.updated_at
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog
