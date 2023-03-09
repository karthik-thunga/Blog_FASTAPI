from fastapi import FastAPI
from .routers import users, posts, auth, votes, comments
from . import models
from .database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comments.router)

# from fastapi.params import Body
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# database connection
# while True:
#     try:
#         conn = psycopg2.connect(database='fastapi_postgres', user='postgres', password='9036')
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#         print(f"Connection to database was successful")
#         break
#     except Exception as exp:
#         print(f"Connection to database was not successful. \nERROR: {exp}")
#         time.sleep(3)
