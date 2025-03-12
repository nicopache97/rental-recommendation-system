import sqlite3
from faker import Faker
import numpy as np
import re
import os
import json
from datetime import datetime

# Initialize Faker
fake = Faker()

# Connect to the database

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'db', 'tables.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Tables
def create_tables():
    """Crea las tablas necesarias si no existen"""

    # Tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefono TEXT,
        redes_sociales TEXT,
        fecha_nacimiento TEXT,
        genero TEXT,
        ocupacion TEXT,
        deportes TEXT,
        presupuesto_maximo REAL,
        habitos_limpieza INTEGER CHECK(habitos_limpieza BETWEEN 1 AND 5),
        horario_trabajo TEXT,
        tiene_mascota INTEGER,
        acepta_mascota INTEGER,
        es_fumador INTEGER,
        acepta_fumador INTEGER,
        intereses TEXT,
        preferencias_roommate TEXT,
        fecha_registro TEXT,
        ultima_actualizacion TEXT,
        activo INTEGER DEFAULT 1
    )
    ''')

    # Tabla de similitudes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS similitudes (
        user_id_1 INTEGER,
        user_id_2 INTEGER,
        score_similitud REAL,
        fecha_calculo TEXT,
        PRIMARY KEY (user_id_1, user_id_2),
        FOREIGN KEY (user_id_1) REFERENCES usuarios(user_id),
        FOREIGN KEY (user_id_2) REFERENCES usuarios(user_id)
    )
    ''')
    conn.commit()

# Function to generate a single user
def generate_user():
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

# Funcion de puntuacion de usuarios
def recomendacion_score(usr1, usr2):
    score=0.0
    # Redes sociales [parametro 4]
    if usr1[4] and usr2[4]:  # Ambos tienen redes sociales definidas
        score += 0.6
    elif not usr1[4] and not usr2[4]:  # Ninguno tiene redes sociales definidas
        score += 0.5


    # Edad [parametro 5]
    try:
        # Convierte las fechas de nacimiento a objetos datetime
        fecha_nacimiento1 = datetime.fromisoformat(usr1[5])
        fecha_nacimiento2 = datetime.fromisoformat(usr2[5])

        # Calcula la diferencia de edad en años decimales
        diferencia_edad=(fecha_nacimiento1-fecha_nacimiento2).days / 365.25

        # Aplica la función exponencial para la similitud de edad
        score += 2 * np.exp(-abs(diferencia_edad) / 3)

    except (TypeError, ValueError, IndexError):
        pass  # Ignora si la fecha de nacimiento no es válida o no está presente

    # Género [parametro 6]
    if usr1[6] and usr2[6] and usr1[6] == usr2[6]:
        score += 1.0

    # Ocupación [parametro 7]
    if usr1[7] and usr2[7] and comparador_cadena_palabras(usr1[7], usr2[7]):
        score += 2.0

    # Deportes [parametro 8]
    if usr1[8] and usr2[8] and comparador_cadena_palabras(usr1[8], usr2[8]):
        score += 2.0

    # Presupuesto [parametro 9]
    if abs(usr1[9] - usr2[9]) < 100:
        score += 1.0

    # Hábitos de limpieza [parametro 10]
    if usr1[10] and usr2[10] and usr1[10] == usr2[10]:  #si comparten tipo limpieza
        score += 1.0

    if usr1[10] and usr2[10] and abs(usr1[10]-usr2[10])==1:  # si son similares
        score += 0.8

    if usr1[10] and usr2[10] and abs(usr1[10]-usr2[10])==2:  # si difieren por dos
        score += 0.4

    # Horario de trabajo [parametro 11]
    if usr1[11] and usr2[11] and usr1[11] == usr2[11]:
        score += 1

    # Mascotas [parametro 12:tiene_mascota] [parametro 13:acepta_mascota]
    if usr1[12] and not usr2[13]:  # usr1 tiene mascota y usr2 no la acepta
        score -= 2.0
    if usr2[12] and not usr1[13]:  # usr2 tiene mascota y usr1 no la acepta
        score -= 2.0
    if usr1[13] and usr2[12]:  # usr1 acepta mascota y usr2 tiene una
        score += 0.5
    if usr2[13] and usr1[12]:  # usr2 acepta mascota y usr1 tiene una
        score += 0.5
    if usr1[13] == usr2[13]:  # Comparten gusto por mascota
        score += 1.0

    # Fumador [parametro 12:es_fumador] [parametro 13:acepta_fumador]
    if usr1[14] and not usr2[15]:  # usr1 fuma y usr2 no lo acepta
        score -= 2.0
    if usr2[14] and not usr1[15]:  # usr2 fuma y usr1 no lo acepta
        score -= 2.0
    if usr1[15] and usr2[14]:  # usr1 acepta fumador y usr2 fuma
        score += 0.5
    if usr2[15] and usr1[14]:  # usr2 acepta fumador y usr1 fuma
        score += 0.5
    if usr1[15] == usr2[15]:  # Comparten gusto sobre fumar
        score += 1.0

    # Intereses [parametro 16]
    try:
        intereses1 = json.loads(usr1[16]) if usr1[16] else [] # Si usr1[16] es None o una cadena vacía, inicializar intereses1 como una lista vacía.
        intereses2 = json.loads(usr2[16]) if usr2[16] else [] # Lo mismo para intereses2

        if intereses1 and intereses2 and comparador_cadena_palabras(intereses1, intereses2):
           score += 2.0
    except (json.JSONDecodeError, TypeError):
        pass  # Ignora si los intereses no son un JSON válido o si no están presentes

    # Preferencias de roommate [parametro 17]
    try:
        preferencias1 = json.loads(usr1[17]) if usr1[17] else {}
        preferencias2 = json.loads(usr2[17]) if usr2[17] else {}

        if preferencias1 and preferencias2 and comparador_cadena_palabras(preferencias1, preferencias2):
           score += 2.0
    except (json.JSONDecodeError, TypeError):
        pass  # Ignora si las preferencias no son un JSON válido o si no están presentes

    return score

    #Compara dos cadenas de texto (o listas) y busca palabras en común.
def comparador_cadena_palabras(str1, str2):
    def _extract_words(data):
        """Extrae palabras de una cadena, lista o diccionario."""
        if isinstance(data, str):
            return re.findall(r'\b\w+\b', data.lower())
        elif isinstance(data, list):
            return re.findall(r'\b\w+\b', ", ".join(data).lower())
        elif isinstance(data, dict):
            words = []
            for value in data.values():
                if isinstance(value, str):
                    words.extend(re.findall(r'\b\w+\b', value.lower()))
                elif isinstance(value, list):
                    words.extend(re.findall(r'\b\w+\b', ", ".join(value).lower()))
            return words
        else:
            return []

    palabras1 = _extract_words(str1)
    palabras2 = _extract_words(str2)

    # Buscar palabras en común
    palabras_comunes = set(palabras1) & set(palabras2)

    # Si hay al menos una palabra en común, retornar True
    return len(palabras_comunes) > 0

### PROGRAMA PRINCIPAL
# crear tablas, cargar usuarios y calcular scores

create_tables()
# Insert 100 users
for _ in range(100):
    user = generate_user()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, email, telefono, redes_sociales, fecha_nacimiento, genero, ocupacion, deportes, presupuesto_maximo, habitos_limpieza, horario_trabajo, tiene_mascota, acepta_mascota, es_fumador, acepta_fumador, intereses, preferencias_roommate, fecha_registro, ultima_actualizacion, activo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list(user.values()))
    except sqlite3.IntegrityError:  # Handle potential unique constraint violations
        pass  # Skip if email is already in the database
conn.commit()

# deshabilita 3 usuarios
user_ids = (50, 51, 52)
cursor.execute("UPDATE usuarios SET activo = 0 WHERE user_id IN (?, ?, ?)", user_ids)
conn.commit()

print("Se han creado 100 usuarios de forma correcta, 3 inactivos")

# Obtener los IDs de usuarios activos
cursor.execute("SELECT * FROM usuarios WHERE activo = 1")
usuarios_activos = cursor.fetchall()

# Crear una lista para almacenar las similaridades
similaridades = []

# Calcular la similitud entre todos los pares de usuarios activos
for i in range(len(usuarios_activos)):
    for j in range(i + 1, len(usuarios_activos)):
        usr1 = usuarios_activos[i]
        usr2 = usuarios_activos[j]
        score = recomendacion_score(usr1, usr2)
        similaridades.append((usr1[0], usr2[0], score))

# Insertar las similaridades en la tabla 'similaridades'
for usr1_id, usr2_id, score in similaridades:
    try:
        cursor.execute("INSERT INTO similitudes (user_id_1, user_id_2, score_similitud, fecha_calculo) VALUES (?, ?, ?, datetime('now'))", (usr1_id, usr2_id, score))
    except sqlite3.IntegrityError:
        pass

print("se calcularon las recomendaciones de todos los usuarios")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
