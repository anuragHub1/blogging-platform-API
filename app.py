from fastapi import FastAPI
from src.routers import post

app=FastAPI(
    title="Blog API",
    description="Simple Blog API using FastAPI and MySQL",
    version="1.0.0"
)

app.include_router(post.router)

@app.get("/")
def root():
    return {"message":"blog api running"}