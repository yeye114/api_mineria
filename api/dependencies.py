from pydantic import BaseModel
from datetime import datetime
from typing import List

class SensorReading(BaseModel):
    id: str
    type: str
    value: float
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "type": "temp",
                "value": 28.5,
                "timestamp": "2025-04-01T17:14:10.897Z"
            }
        }