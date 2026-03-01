from pydantic import BaseModel
from typing import List,Generic,TypeVar

T=TypeVar("T")

class PaginatedResponse(BaseModel,Generic[T]):
    total:int
    page:int
    limit:int
    items:List[T]