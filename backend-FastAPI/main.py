from db_manager import DBManager #importo la clase custom de manejo BD
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json

app = FastAPI()

# Modelo de usuario usando Pydantic
class User(BaseModel):
    nombre: str
    email: str
    telefono: str
    redes_sociales: str
    fecha_nacimiento: str
    genero: str
    ocupacion: str
    deportes: str
    presupuesto_maximo: float
    habitos_limpieza: int
    horario_trabajo: str
    tiene_mascota: bool
    acepta_mascota: bool
    es_fumador: bool
    acepta_fumador: bool
    intereses: str
    preferencias_roommate: str
    fecha_registro: str
    ultima_actualizacion: str
    activo: int

@app.post("/")
async def insert_user(user: User):
    """
    Inserta un nuevo usuario y actualiza las similitudes en la base de datos.
    """

    # Verificar si el correo ya existe
    if db.mail_exist(user.email):
        raise HTTPException(status_code=400, detail="El correo ya existe")

    # Insertar nuevo usuario en la base de datos
    new_id = db.insert_user(user.dict())
    
    # Obtener la lista de IDs de usuarios activos
    list_id = db.get_active_users_id().
    
    # Calcular y registrar similitudes entre el nuevo usuario y los demás
    for i in list_id:
        score = db.calculate_similarity(new_id, i)
        db.insert_similarity(new_id, i, score)
    
    # Confirmar los cambios en la base de datos
    db.commit()
    
    return {"message": f"Usuario insertado con ID {new_id} y similitudes calculadas con éxito"}
