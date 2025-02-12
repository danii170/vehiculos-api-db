from datetime import date
from sqlmodel import SQLModel, Field

class Vehiculo(SQLModel, table=True):
    matricula: int  = Field(default=None, primary_key=True)
    modelo: str = Field(index=True, max_length=50)
    kilometraje: float = Field(nullable=True)