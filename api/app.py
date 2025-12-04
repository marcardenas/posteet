from api.authn import register_routes, register_middlewares
from fastapi import FastAPI

app = FastAPI()

register_middlewares(app)
register_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
