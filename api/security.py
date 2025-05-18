from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    valid_keys = os.getenv("API_KEYS", "defaultkey").split(",")
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o faltante"
        )
    return api_key