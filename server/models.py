from pydantic import BaseModel

class DataQuery(BaseModel):
    latitude: float
    longitude: float
    year: int