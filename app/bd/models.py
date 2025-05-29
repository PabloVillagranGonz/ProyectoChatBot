from sqlalchemy import Column, Integer, String
from app.bd.database import Base 

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)
    categoria = Column(String, nullable=False)

