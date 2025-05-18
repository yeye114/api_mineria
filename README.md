# API REST para Proyecto IoT de Minería

API desarrollada con FastAPI para acceso remoto a datos de sensores en entornos mineros.

## Requisitos

- Python 3.8+
- MongoDB 4.4+
- FastAPI
- Motor (Async MongoDB driver)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`

## Configuración

1. Asegúrate de que MongoDB esté corriendo en `mongodb://localhost:27017`
2. Configura la base de datos en `api/dependencies.py`
3. Configura la API Key en `api/security.py` (en producción usa variables de entorno)

## Uso

1. Iniciar el servidor: `uvicorn api.main:app --reload`
2. Acceder a la documentación interactiva: `http://localhost:8000/docs`

## Endpoints

- `GET /lecturas`: Obtener todas las lecturas (paginadas)
- `GET /lecturas/{id}`: Obtener una lectura específica
- `GET /lecturas/filtro`: Filtrar lecturas por parámetros

## Autenticación

Incluir el header `X-API-KEY` con el valor configurado en `security.py`