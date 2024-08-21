from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from Group import database, crud, models, schemas
from Group.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/user/", response_model=schemas.ShowUser)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(detail='User not found',status_code=status.HTTP_404_NOT_FOUND)
    db.delete(user)
    db.commit()
    return {'detail': 'User deleted'}
@app.put("/user/{user_id}", status_code= status.HTTP_202_ACCEPTED)
def update(user_id: int , request: schemas.CreateUser, db: Session = Depends(get_db)):
    pass
@app.get("/user/", response_model=list[schemas.ShowUser])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.ShowUser)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
