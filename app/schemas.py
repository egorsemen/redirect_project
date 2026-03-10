from pydantic import BaseModel, HttpUrl, ConfigDict


class URLBase(BaseModel):
    url: HttpUrl  


class URLCreate(URLBase):
    pass


class URLResponse(BaseModel):
    short_id: str
    model_config = ConfigDict(from_attributes=True)


class URLStats(BaseModel):
    original_url: str
    short_id: str
    clicks: int
    model_config = ConfigDict(from_attributes=True)