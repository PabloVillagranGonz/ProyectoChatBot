from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.predict import PreguntaEntrada, PrediccionRespuesta
from app.auth import Token, User, fake_users_db
from app.bd.database import SessionLocal
from app.bd.models import Prediccion
from app import model
from app.auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)  # funciones de auth

# Variables de configuración
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Dependencia para sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de autenticación
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta de prueba
@router.get("/prueba")
def ruta_prueba():
    return {"mensaje": "La API funciona correctamente"}

# Ruta ping
@router.get("/ping")
def ruta_ping():
    return {"status": "ok"}


@router.post("/predict", response_model=PrediccionRespuesta)
async def predecir_categoria(
    pregunta: PreguntaEntrada,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not pregunta.texto:
        raise HTTPException(status_code=400, detail="El texto de la pregunta no puede estar vacío")

    try:
        categoria = model.realizar_prediccion(pregunta.texto)
        nueva_prediccion = Prediccion(texto=pregunta.texto, categoria=categoria)
        db.add(nueva_prediccion)
        db.commit()
        db.refresh(nueva_prediccion)
        return {"texto": pregunta.texto, "categoria": categoria}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {str(e)}")
