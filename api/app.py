from api.authn import register_routes, register_middlewares
from api.models import PostitContentModel, PostitResponseModel
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
    response_model=PostitResponseModel,
)
async def create_message(
    item: PostitContentModel, user: User = Depends(current_active_user)
):
    user_content = mongo_database[str(user.id)]
    total_content = len(list(user_content.find()))

    payload = item.model_dump()
    payload["postit_id"] = total_content + 1  # Simple incremental ID

    user_content.insert_one(payload)

    return payload


@app.get(
    "/posteet",
    status_code=status.HTTP_200_OK,
    response_model=list[PostitResponseModel],
)
async def read_posteet_list(user: User = Depends(current_active_user)):
    user_content = mongo_database[str(user.id)]
    docs = user_content.find()

    if not docs:
        return JSONResponse(
            status_code=404, content={"error": "No Posteets found"}
        )

    docs_json = bson.json_util.dumps(docs)

    print(docs_json)

    return json.loads(docs_json)


@app.get(
    "/posteet/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PostitResponseModel,
)
async def read_posteet(id: int, user: User = Depends(current_active_user)):
    user_content = mongo_database[str(user.id)]
    doc = user_content.find_one({"postit_id": id})
    if not doc:
        return JSONResponse(
            status_code=404, content={"error": "Posteet not found"}
        )

    doc_json = bson.json_util.dumps(doc)
    return json.loads(doc_json)


@app.put("/posteet/{id}", response_model=PostitContentModel)
async def update_posteet(id: int):
    return {"message": "Posteet updated successfully."}


@app.delete("/posteet/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_posteet(id: int, user: User = Depends(current_active_user)):
    user_content = mongo_database[str(user.id)]
    query = {"postit_id": id}
    result = user_content.delete_one(query)

    if result.deleted_count == 0:
        return JSONResponse(
            status_code=404, content={"error": "Posteet not found"}
        )
