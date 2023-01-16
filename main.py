import uvicorn
from fastapi import FastAPI

from db.db_conf import engine, Base
from routers import auth, common, user, post, reaction

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(common.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(reaction.router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app", host='0.0.0.0',
        port=5000, reload=False
    )
