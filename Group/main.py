from fastapi import FastAPI
from Group import models
from Group.database import engine
from Group.routers import user, authentication, group, role, member, join_request, blog

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(group.router)
app.include_router(role.router)
app.include_router(member.router)
app.include_router(join_request.router)
app.include_router(blog.router)