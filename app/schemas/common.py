from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseOK(BaseModel, Generic[T]):
    status: str = "ok"
    data: T

class ResponseError(BaseModel):
    status: str = "error"
    message: str
