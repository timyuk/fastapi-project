from pydantic import BaseModel, HttpUrl


class UrlCreate(BaseModel):
    url: HttpUrl

class UrlReturn(BaseModel):
    id: int
    url: HttpUrl


