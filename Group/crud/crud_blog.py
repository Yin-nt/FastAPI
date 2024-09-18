from sqlalchemy.orm import Session
from Group import models, schemas


def create_blog(db: Session, blog: schemas.CreateBlog):
    db_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        group_id=blog.group_id,
        author_id=blog.author_id,
        permission=blog.permission,
        create_at=blog.create_at,
        update_at=blog.update_at
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def update_blog(db: Session, blog_id: int, blog: schemas.UpdateBlog):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    db_blog.title = blog.title
    db_blog.content = blog.content
    db_blog.permission = blog.permission
    db_blog.update_at = blog.update_at
    db.commit()
    db.refresh(db_blog)
    return db_blog


def delete_blog(db: Session, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    db.delete(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_blog(db: Session, author_id: int, group_id: int):
    return db.query(models.Blog).filter(models.Blog.author_id == author_id,
                                        models.Blog.group_id == group_id).first()


def get_all_blogs_of_author(db: Session, author_id: int, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).filter(models.Blog.author_id == author_id,
                                        models.Blog.group_id == group_id).offset(skip).limit(limit).all()


def get_all_blogs(db: Session, user_id: int, group_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).filter(models.Blog.group_id == group_id,
                                        (models.Blog.permission == True) | (models.Blog.author_id == user_id)
                                        ).offset(skip).limit(limit).all()


def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def is_blog_exist(db: Session, title: str, group_id: int, author_id: int):
    return db.query(models.Blog).filter(
        models.Blog.title == title,
        models.Blog.group_id == group_id,
        models.Blog.author_id == author_id
    ).first()
