from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import Annotated

from src.models.vehiculo import Vehiculo
from src.data.db import get_session, init_db
from sqlmodel import Field,Session,SQLModel,create_engine,select

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

SessionDep =Annotated[Session, Depends(get_session)]

#Crear
@app.post("/vehiculos", response_model=Vehiculo)
async def nuevo_vehiculo(vehiculo: Vehiculo, session: SessionDep):
    session.add(vehiculo)
    session.commit()
    session.refresh(vehiculo)
    return vehiculo

#Leer
@app.get("/vehiculos", response_model=list[Vehiculo])
async def lista_vehiculos(session: SessionDep):
    vehiculo = session.exec(select(Vehiculo)).all()
    return vehiculo


#Borrar
@app.delete("/vehiculos/{matricula}")
def borrar_vehiculo (matricula: int, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    session.delete(vehiculo_encontrado)
    session.commit()
    return "Vehiculo eliminado"


#Modificar
@app.put("/vehiculos")
def borrar_vehiculo (vehiculo: Vehiculo, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, vehiculo.matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    
    vehiculo_encontrado.modelo = vehiculo.modelo 
    vehiculo_encontrado.kilometraje = vehiculo.kilometraje 

    session.commit()
    return "Vehiculo modificado"


#Patch
@app.patch("/vehiculos/{matricula}", response_model=Vehiculo)
def cambio_vehiculo(matricula: int, vehiculo: Vehiculo, session: SessionDep):
    vehiculo_encontrado = session.get(Vehiculo, vehiculo.matricula)
    if not vehiculo_encontrado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    
    vehiculo_data = vehiculo.model_dump(exclude_unset=True)
    vehiculo_encontrado.sqlmodel_update(vehiculo_data)
    session.add(vehiculo_encontrado)
    session.commit()
    session.refresh(vehiculo_encontrado)
    return vehiculo_encontrado


#Media kilómetros
@app.get("/vehiculos/mediakm")
async def calcular_media_kilometraje(session: SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all()
    
    if not vehiculos:
        raise HTTPException(status_code=404, detail="No hay vehículos registrados")
    
    total_km = 0

    for vehiculo in vehiculos:
        total_km += vehiculo.kilometraje
    
    media = total_km / len(vehiculos)
    return {"media_km": f"{media:.2f}"}


#Menos kilómetros
@app.get("/vehiculos/menoskm", response_model=Vehiculo)
async def vehiculo_menos_km(session: SessionDep):
    vehiculos = session.exec(select(Vehiculo)).all()
    
    if not vehiculos:
        raise HTTPException(status_code=404, detail="No hay vehículos registrados")
    

    vehiculo_menos_km= None

    for vehiculo in vehiculos:
        if vehiculo_menos_km is None or vehiculo.kilometraje< vehiculo_menos_km.kilometraje:
            vehiculo_menos_km = vehiculo
    return vehiculo_menos_km    
     