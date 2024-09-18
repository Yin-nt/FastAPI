from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Group import database, schemas
from Group.crud import crud_blog, crud_user, crud_member
from Group.core import oauth2

router = APIRouter(
    tags=["Blogs"]
)
get_db = database.get_db


@router.post("/blog", response_model=schemas.ShowBlog)
def create_blog(blog: schemas.CreateBlog,
                current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    author = crud_user.get_user_by_email(db=db, email=current_user.username)
    db_blog = crud_blog.is_blog_exist(db=db, title=blog.title, group_id=blog.group_id, author_id=author.id)
    if db_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog đã tồn tại.")
    return crud_blog.create_blog(db, blog=blog)


@router.put("/blog/{blog_id}", response_model=schemas.ShowBlog)
def update_blog(blog_id: int,
                blog: schemas.UpdateBlog,
                current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    author = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not author:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    db_blog = crud_blog.get_blog_by_id(db=db, blog_id=blog_id)
    if not db_blog:
        raise HTTPException(status_code=404, detail="Không tìm thấy blog.")
    if author.id != db_blog.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền chỉnh sửa.")
    return crud_blog.update_blog(db=db, blog_id=blog_id, blog=blog)


@router.delete("/blog/{blog_id}", response_model=schemas.ShowBlog)
def delete_blog(blog_id: int, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    db_blog = crud_blog.get_blog_by_id(db=db, blog_id=blog_id)
    if user.id != db_blog.author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xóa blog.")
    return crud_blog.delete_blog(db=db, blog_id=blog_id)


# xem blog trong nhóm public và private nếu là author
@router.get("/blog/{blog_id}", response_model=schemas.ShowBlog)
def get_1_blog_public(blog_id: int, db: Session = Depends(get_db),
                      current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    db_blog = crud_blog.get_blog_by_id(db=db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy blog.")
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    member = crud_member.get_member_by_user_and_group_id(db=db, user_id=user.id, group_id=db_blog.group_id)
    if not member or not member.is_approve:
        raise HTTPException(status_code=403, detail="Bạn chưa là thành viên của nhóm.")
    if not db_blog.permission and user.id != db_blog.author_id:
        raise HTTPException(status_code=403, detail="Blog đang ở chế độ private.")
    return db_blog


@router.get("/group/{group_id}/blogs", response_model=list[schemas.ShowBlog])
def get_group_blogs(group_id: int, skip: int = 0, limit: int = 25, db: Session = Depends(get_db),
                    current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    member = crud_member.get_member_by_user_and_group_id(db=db, user_id=user.id, group_id=group_id)
    if not member or not member.is_approve:
        raise HTTPException(status_code=403, detail="Bạn chưa là thành viên của nhóm.")
    blogs = crud_blog.get_all_blogs(db=db, user_id=user.id, group_id=group_id, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(status_code=404, detail="Không có blog nào xem được.")
    return blogs



# Xem blog cua ca nhan trong 1 group
@router.get("/user/group/{group_id}/blogs", response_model=list[schemas.ShowBlog])
def show_blogs_of_author(group_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = crud_user.get_user_by_email(db=db, email=current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Không tồn tại user.")
    member = crud_member.get_member_by_user_and_group_id(db=db, user_id=user.id, group_id=group_id)
    if not member or not member.is_approve:
        raise HTTPException(status_code=404, detail="Bạn chưa là thành viên của nhóm.")
    blogs = crud_blog.get_all_blogs_of_author(db=db, author_id=user.id, group_id=group_id, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(status_code=404, detail="User không có blog nào.")
    return blogs
