import os
from faker import Faker
import json
from datetime import datetime

# Importar la clase DBManager
from db_manager import DBManager

# Initialize Faker
fake = Faker()

def generate_user():
    """Genera un usuario de prueba con datos aleatorios."""
    user = {
        'nombre': fake.name(),
        'email': fake.email(),
        'telefono': fake.phone_number(),
        'redes_sociales': fake.user_name(),
        'fecha_nacimiento': fake.date_of_birth(minimum_age=18, maximum_age=40).isoformat(),
        'genero': fake.random_element(elements=('M', 'F')),
        'ocupacion': fake.job(),
        'deportes': fake.random_element(elements=('Yoga', 'Running', 'Natación', 'Fútbol', 'Baloncesto', '')),
        'presupuesto_maximo': fake.pyfloat(min_value=300, max_value=1000, right_digits=2),
        'habitos_limpieza': fake.random_int(min=1, max=5),
        'horario_trabajo': fake.random_element(elements=('9:00-17:00', '10:00-18:00', '8:00-16:00', '')),
        'tiene_mascota': fake.boolean(),
        'acepta_mascota': fake.boolean(),
        'es_fumador': fake.boolean(),
        'acepta_fumador': fake.boolean(),
        'intereses': json.dumps(fake.words(nb=3)),
        'preferencias_roommate': json.dumps({'edad_min': fake.random_int(min=18, max=30),
                                            'edad_max': fake.random_int(min=30, max=50)}),
        'fecha_registro': datetime.now().isoformat(),
        'ultima_actualizacion': datetime.now().isoformat(),
        'activo': 1
    }
    return user

def main():
    """Función principal para inicializar la base de datos."""
    # Definir la ruta de la base de datos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, '..', 'db', 'tables.db')
    
    # Asegurar que el directorio de la base de datos existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Crear una instancia del gestor de base de datos
    with DBManager(db_path) as db:
        # Crear las tablas
        db.create_tables()
        
        # Generar e insertar 100 usuarios
        inserted = 0
        for _ in range(100):
            user = generate_user()
            db.insert_user(user)
        db.commit()
        
        print(f"Se han creado 100 usuarios de forma correcta")
        
        # Desactivar 3 usuarios
        db.deactivate_users([50, 51, 52])
        print("Se han desactivado 3 usuarios (IDs: 50, 51, 52)")
        
        # Calcular similitudes entre todos los usuarios activos
        similarities_count = db.calculate_all_similarities()
        print(f"Se calcularon {similarities_count} recomendaciones entre usuarios")

if __name__ == "__main__":
    main()
