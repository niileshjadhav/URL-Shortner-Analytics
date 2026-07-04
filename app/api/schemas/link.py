from pydantic import BaseModel, HttpUrl
from datetime import datetime

class LinkCreate(BaseModel):
    target_url : HttpUrl
    custom_code : str | None = None

class LinkResponse(BaseModel):
    code : str
    target_url : str
    created_at : datetime

    class Config:
        from_attributes = True