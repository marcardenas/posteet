from api.authn import register_routes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS: read ALLOWED_ORIGINS env var (comma separated). Default to allow all in dev.
_allowed = os.getenv("ALLOWED_ORIGINS")
if _allowed:
    origins = [o.strip() for o in _allowed.split(",") if o.strip()]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_routes(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}