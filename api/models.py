from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, Union

class SensorReading(BaseModel):
    id: str
    type: str
    value: Union[float, str]  # Acepta float o string
    timestamp: datetime

    @validator('value', pre=True)
    def convert_value(cls, v):
        try:
            return float(v)
        except (ValueError, TypeError):
            return str(v) if v is not None else None

    @validator('timestamp', pre=True)
    def parse_mongo_date(cls, v):
        if isinstance(v, dict) and '$date' in v:
            return datetime.fromisoformat(v['$date'].replace('Z', '+00:00'))
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "type": "temp",
                "value": 28.5,
                "timestamp": "2025-04-01T17:14:10.897Z"
            }
        }
