from typing import List
from pydantic import BaseModel


class MSFSData(BaseModel):
    name: str
    value: float

class MSFSDataList(BaseModel):
    command: str="update_data"
    data: List[MSFSData]