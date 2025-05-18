from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Union
from dotenv import load_dotenv
import os
import urllib.parse
from bson import ObjectId

# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
app = FastAPI(
    title="API de Sensores para Minería",
    description="API REST para acceder a datos de sensores IoT en entornos mineros",
    version="1.0.0"
)

# Configuración CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de seguridad
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Modelo Pydantic
class SensorReading(BaseModel):
    id: str
    type: str
    value: Union[float, str] 
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

# Conexión a MongoDB
def get_db():
    try:
        client = MongoClient(
            os.getenv("MONGODB_URI", "mongodb+srv://cira3726:xdW0f8ccY7GjDHWP@cluster0.wnffexy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"),
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            maxPoolSize=100
        )
        client.admin.command('ping')
        db = client[os.getenv("DB_NAME", "sensor_data")]
        return db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión a MongoDB: {str(e)}"
        )

# Autenticación
def get_api_key(api_key: str = Depends(api_key_header)):
    valid_keys = os.getenv("API_KEYS", "defaultkey").split(",")
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o faltante"
        )
    return api_key

# Endpoints como solicitaste
@app.get("/readings/", response_model=List[SensorReading])
async def get_all_readings(
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    readings = list(collection.find().limit(1000))
    return [{
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    } for reading in readings]

@app.get("/readings/filter/", response_model=List[SensorReading])
async def filter_readings(
    field: str = Query(..., description="Campo por el que filtrar"),
    value: str = Query(..., description="Valor del campo a buscar"),
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    
    # Convertir value a número si es posible
    try:
        value = float(value) if "." in value else int(value)
    except ValueError:
        pass
    
    query = {field: value}
    readings = list(collection.find(query).limit(1000))
    
    return [{
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    } for reading in readings]

@app.get("/readings/{reading_id}", response_model=SensorReading)
async def get_reading_by_id(
    reading_id: str,
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    
    try:
        reading = collection.find_one({"_id": ObjectId(reading_id)})
    except:
        reading = None
    
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    
    return {
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    }

# Endpoints como solicitaste
@app.get("/readings/", response_model=List[SensorReading])
async def get_all_readings(
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    readings = list(collection.find().limit(1000))
    return [{
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    } for reading in readings]

@app.get("/readings/filter/", response_model=List[SensorReading])
async def filter_readings(
    field: str = Query(..., description="Campo por el que filtrar"),
    value: str = Query(..., description="Valor del campo a buscar"),
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    
    # Convertir value a número si es posible
    try:
        value = float(value) if "." in value else int(value)
    except ValueError:
        pass
    
    query = {field: value}
    readings = list(collection.find(query).limit(1000))
    
    return [{
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    } for reading in readings]

@app.get("/readings/{reading_id}", response_model=SensorReading)
async def get_reading_by_id(
    reading_id: str,
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    
    try:
        reading = collection.find_one({"_id": ObjectId(reading_id)})
    except:
        reading = None
    
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    
    return {
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    }

@app.post("/readings/", response_model=SensorReading)
async def create_reading(
    reading: SensorReading,
    api_key: str = Depends(get_api_key),
    db: MongoClient = Depends(get_db)
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    
    reading_dict = reading.dict()
    # Eliminamos el id si viene en el request (MongoDB lo generará)
    reading_dict.pop("id", None)
    
    # Aseguramos que el timestamp sea datetime
    if isinstance(reading_dict["timestamp"], str):
        reading_dict["timestamp"] = datetime.fromisoformat(reading_dict["timestamp"])
    
    result = collection.insert_one(reading_dict)
    
    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Error al crear la lectura")
    
    return {
        "id": str(result.inserted_id),
        "type": reading_dict["type"],
        "value": reading_dict["value"],
        "timestamp": reading_dict["timestamp"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/datos", response_model=List[SensorReading])
async def datos_publicos(
    db: MongoClient = Depends(get_db)  # <-- SIN API KEY
):
    collection = db[os.getenv("COLLECTION_NAME", "readings")]
    readings = list(collection.find().limit(1000))
    return [{
        "id": str(reading["_id"]),
        "type": reading["type"],
        "value": reading["value"],
        "timestamp": reading["timestamp"]
    } for reading in readings]

