from app.authn import register_routes

from fastapi import FastAPI

app = FastAPI()

register_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}