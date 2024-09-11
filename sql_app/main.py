from fastapi import FastAPI
from sql_app import models
from sql_app.database import engine
from sql_app.routers import item, user, authentication

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(item.router)
app.include_router(user.router)
app.include_router(authentication.router)


#Kiểm tra xem bảng có tồn tại không, nếu không thì tạo bảng mới, nếu có thì giữ nguyên

# Dependency
#tạo sự phụ thuộc (tạo 1 SQLAlchemy mới vs 1 yêu cầu duy nhất và đóng lại khi hoàn tất)
# def get_db():
#     db = SessionLocal()
#     try: # đảm bảo session luôn đóng ngay cả khi có ngoại lệ
#         yield db
#     finally:
#         db.close()

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)
#
# @app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first() # first() returns the first  that match the
#     # condition
#     if not user:
#         raise HTTPException(detail='User not found',status_code=status.HTTP_404_NOT_FOUND)
#     db.delete(user)
#     db.commit()
#     return {'detail': 'User deleted'}
# @app.put("/users/{user_id}", status_code= status.HTTP_202_ACCEPTED)
# def update(id, request: schemas.User, df: Session = Depends(get_db)):
#     pass
# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @app.get("/users/{user_id}", response_model=schemas.ShowUsers) # only show email and item
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
