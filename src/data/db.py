from src.models.vehiculo import Vehiculo
from sqlmodel import SQLModel, Session, create_engine
import os

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "fastapi-db-coches" 
db_port: int = 3306  
db_name: str = "vehiculosdb" 

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(os.getenv("db_url",DATABASE_URL), echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Vehiculo(matriucla="1234ABC", modelo="Seat Leon", kilometraje=0))
        session.add(Vehiculo(matriucla="5678DEF", modelo="Audi A3", kilometraje=125000))
        session.add(Vehiculo(matriucla="9123GHI", modelo="Mercedes Benz", kilometraje=20000))
        session.commit()