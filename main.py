from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.routers import predict
from app.bd.database import Base, engine
from app.bd import models
from app.core.exceptions import (
    custom_http_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)
# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de ChatBot",
    description="API para clasificar preguntas y almacenarlas",
    version="1.0"
)

@app.get("/")
async def read_root():
    return {"Mensaje": "Bienvenido a la API de ChatBot. Ve a /docs para la documentacion."}

# Incluir router de predict
app.include_router(predict.router)


# Registra los handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)