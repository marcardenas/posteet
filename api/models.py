from pydantic import BaseModel

class PostitContentModel(BaseModel):
    content: str
    position_x: float
    position_y: float
    date: str
