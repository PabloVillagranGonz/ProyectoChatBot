from pydantic import BaseModel

class PreguntaEntrada(BaseModel):
    texto: str

class PrediccionRespuesta(BaseModel):
    texto: str
    categoria: str

