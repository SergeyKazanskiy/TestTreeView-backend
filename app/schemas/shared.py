from pydantic import BaseModel


class ResponseOk(BaseModel):
    isOk: bool

class ResponseId(BaseModel):
    id: int
