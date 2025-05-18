from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Union

class SensorReading(BaseModel):
    id: str
    type: str
    value: Union[float, str]
    timestamp: datetime

    @field_validator('value', mode='before')
    @classmethod
    def convert_value(cls, v):
        try:
            return float(v)
        except (ValueError, TypeError):
            return str(v) if v is not None else None

    @field_validator('timestamp', mode='before')
    @classmethod
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

