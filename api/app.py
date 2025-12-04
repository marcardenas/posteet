from api.authn import register_routes, register_middlewares
from api.models import PostitContentModel
from api.users import current_active_user, User
from api.db import mongo_database
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse

import bson.json_util
import json

app = FastAPI()

register_middlewares(app)
register_routes(app)


@app.post(
    "/posteet",
    status_code=status.HTTP_201_CREATED,
    response_model=PostitContentModel,
)
async def create_message(
    item: PostitContentModel, user: User = Depends(current_active_user)
):
    user_content = mongo_database[str(user.id)]
    total_content = len(list(user_content.find()))

    payload = item.model_dump()
    payload["postit_id"] = total_content + 1  # Simple incremental ID

    print("Payload to insert:", payload)

    user_content.insert_one(payload)

    return payload


@app.get("/posteet/{id}", status_code=status.HTTP_200_OK)
async def read_posteet(id: int, user: User = Depends(current_active_user)):
    user_content = mongo_database[str(user.id)]
    doc = user_content.find_one({"postit_id": id})
    if not doc:
        return JSONResponse(status_code=404, content={"error": "Posteet not found"})

    doc_json = bson.json_util.dumps(doc)
    return json.loads(doc_json)


@app.put("/posteet/{id}", response_model=PostitContentModel)
async def update_posteet(id: int):
    return {"message": "Posteet updated successfully."}


@app.delete("/posteet/{id}")
async def delete_posteet(id: int):
    return {"message": "Posteet deleted successfully."}
