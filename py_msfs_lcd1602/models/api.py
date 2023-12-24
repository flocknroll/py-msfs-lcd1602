from typing import List
from pydantic import BaseModel


class MSFSData(BaseModel):
    name: str
    value: float

class MSFSDataList(BaseModel):
    data: List[MSFSData]