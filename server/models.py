from pydantic import BaseModel

class DataQuery(BaseModel):
    latitude: float
    longetude: float
    year: int