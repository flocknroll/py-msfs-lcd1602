from typing import List
from pydantic import BaseModel


class MSFSData(BaseModel):
    name: str
    value: float

class MSFSDataList(BaseModel):
    data: List[MSFSData]

    @classmethod
    def from_dict(cls, data: dict):
        model = cls()
        model.data = []

        for k, v in data.items():
            pt = MSFSData()
            pt.name = k
            pt.vale = v

        return model