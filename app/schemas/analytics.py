from pydantic import BaseModel

class ClickStats(BaseModel):
    total_clicks : int

class TopReferrers(BaseModel):
    referrer : str
    count : int