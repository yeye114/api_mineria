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
        # Intenta convertir a float, si falla devuelve el valor original
        try:
            return float(v)
        except (ValueError, TypeError):
            return str(v) if v is not None else None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "type": "temp",
                "value": 28.5,
                "timestamp": "2025-04-01T17:14:10.897Z"
            }
        }