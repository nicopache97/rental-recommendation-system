import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Tuple, Any, Optional, Union

class DBManager:
    """
    Clase para gestionar la conexión y operaciones con la base de datos SQLite
    para la aplicación de recomendación de roommates.
    """
    
    def __init__(self, db_path: str = None):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos. Si es None, se usará la ubicación predeterminada.
        """
        if db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, '..', 'db', 'tables.db')
            
            # Asegurar que el directorio de la base de datos existe
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self) -> None:
        """Establece la conexión a la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Error al conectar a la base de datos: {e}")
    
    def disconnect(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def __enter__(self):
        """Soporte para el contexto 'with'."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierre automático al salir del contexto 'with'."""
        self.disconnect()
    
    def execute_query(self, query: str, params: tuple = ()) -> None:
        """
        Ejecuta una consulta SQL sin retorno.
        
        Args:
            query: Consulta SQL a ejecutar.
            params: Parámetros para la consulta.
        """
        if not self.conn:
            self.connect()
        
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error al ejecutar consulta: {e}")
    
    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """
        Ejecuta una consulta SQL múltiples veces con diferentes parámetros.
        
        Args:
            query: Consulta SQL a ejecutar.
            params_list: Lista de tuplas con parámetros para cada ejecución.
        """
        if not self.conn:
            self.connect()
        
        try:
            self.cursor.executemany(query, params_list)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error al ejecutar consulta múltiple: {e}")
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        """
        Ejecuta una consulta y devuelve todos los resultados.
        
        Args:
            query: Consulta SQL a ejecutar.
            params: Parámetros para la consulta.
            
        Returns:
            Lista de tuplas con los resultados.
        """
        if not self.conn:
            self.connect()
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener datos: {e}")
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """
        Ejecuta una consulta y devuelve el primer resultado.
        
        Args:
            query: Consulta SQL a ejecutar.
            params: Parámetros para la consulta.
            
        Returns:
            Tupla con el resultado o None si no hay resultados.
        """
        if not self.conn:
            self.connect()
        
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Error al obtener datos: {e}")
    
    def create_tables(self) -> None:
        """Crea las tablas necesarias si no existen."""
        if not self.conn:
            self.connect()
        
        # Tabla de usuarios
        self.execute_query('''
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
        self.execute_query('''
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

    # place commit after
def insert_user(self, user_data: Dict[str, Any]) -> int:
    """
    Inserta un nuevo usuario en la base de datos y retorna el ID del usuario insertado.
    
    Args:
        user_data: Diccionario con los datos del usuario.
        
    Returns:
        ID del usuario insertado.
    """
    if not self.conn:
        self.connect()

    try:
        # Ejecutar el comando INSERT
        self.cursor.execute(
            """
            INSERT INTO usuarios (
                nombre, email, telefono, redes_sociales, fecha_nacimiento,
                genero, ocupacion, deportes, presupuesto_maximo, habitos_limpieza,
                horario_trabajo, tiene_mascota, acepta_mascota, es_fumador,
                acepta_fumador, intereses, preferencias_roommate, fecha_registro,
                ultima_actualizacion, activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            list(user_data.values())
        )
        new_id = self.cursor.lastrowid         # Obtener el último ID insertado
        self.conn.commit()  # Confirmar la transacción
        return new_id
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Error al insertar el usuario: {e}")
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """
        Actualiza los datos de un usuario existente.
        
        Args:
            user_id: ID del usuario a actualizar.
            user_data: Diccionario con los datos a actualizar.
            
        Returns:
            True si se actualizó correctamente, False en caso contrario.
        """
        if not self.conn:
            self.connect()
        
        try:
            set_clause = ', '.join([f"{k} = ?" for k in user_data.keys()])
            query = f"UPDATE usuarios SET {set_clause} WHERE user_id = ?"
            
            params = list(user_data.values()) + [user_id]
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error al actualizar usuario: {e}")
    
    def get_user_by_id(self, user_id: int) -> Optional[tuple]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario.
            
        Returns:
            Tupla con los datos del usuario o None si no se encuentra.
        """
        return self.fetch_one("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
    
    def get_user_by_email(self, email: str) -> Optional[tuple]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario.
            
        Returns:
            Tupla con los datos del usuario o None si no se encuentra.
        """
        return self.fetch_one("SELECT * FROM usuarios WHERE email = ?", (email,))

    def mail_exist(self, email: str) -> bool:
        """
        Verifica si un correo ya está registrado en la base de datos.
        
        Args:
            email: Email del usuario a verificar.
            
        Returns:
            True si el correo ya existe, False en caso contrario.
        """
        user = self.get_user_by_email(email)
        return user is not None

    
    def get_active_users(self) -> List[tuple]:
        """
        Obtiene todos los usuarios activos.
        
        Returns:
            Lista de tuplas con los datos de los usuarios activos.
        """
        return self.fetch_all("SELECT * FROM usuarios WHERE activo = 1")
    
    def deactivate_users(self, user_ids: List[int]) -> None:
        """
        Desactiva usuarios por sus IDs.
        
        Args:
            user_ids: Lista de IDs de usuarios a desactivar.
        """
        placeholders = ', '.join(['?' for _ in user_ids])
        query = f"UPDATE usuarios SET activo = 0 WHERE user_id IN ({placeholders})"
        self.execute_query(query, tuple(user_ids))
    
    #place commit after
    def insert_similarity(self, user_id_1: int, user_id_2: int, score: float) -> bool:
        """
        Inserta o actualiza la similitud entre dos usuarios.
        
        Args:
            user_id_1: ID del primer usuario.
            user_id_2: ID del segundo usuario.
            score: Puntuación de similitud.
            
        Returns:
            True si se insertó correctamente, False en caso contrario.
        """
        if not self.conn:
            self.connect()
        
        try:
            query = """
            INSERT OR REPLACE INTO similitudes 
            (user_id_1, user_id_2, score_similitud, fecha_calculo) 
            VALUES (?, ?, ?, datetime('now'))
            """
            
            # Asegurar que user_id_1 sea menor que user_id_2 para evitar duplicados
            if user_id_1 > user_id_2:
                user_id_1, user_id_2 = user_id_2, user_id_1
                
            self.cursor.execute(query, (user_id_1, user_id_2, score))
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Error al insertar similitud: {e}")
    
    def get_recommendations(self, user_id: int, limit: int = 5) -> List[tuple]:
        """
        Obtiene las recomendaciones para un usuario.
        
        Args:
            user_id: ID del usuario.
            limit: Número máximo de recomendaciones.
            
        Returns:
            Lista de tuplas con los usuarios recomendados y sus puntuaciones.
        """
        query = """
        WITH all_similarities AS (
            SELECT user_id_1 AS user_id, user_id_2 AS other_user_id, score_similitud
            FROM similitudes
            WHERE user_id_1 = ?
            UNION ALL
            SELECT user_id_2 AS user_id, user_id_1 AS other_user_id, score_similitud
            FROM similitudes
            WHERE user_id_2 = ?
        )
        SELECT u.*, s.score_similitud
        FROM all_similarities s
        JOIN usuarios u ON u.user_id = s.other_user_id
        WHERE u.activo = 1
        ORDER BY s.score_similitud DESC
        LIMIT ?
        """
        
        return self.fetch_all(query, (user_id, user_id, limit))
    
    def calculate_similarity(self, user1: tuple, user2: tuple) -> float:
        """
        Calcula la puntuación de similitud entre dos usuarios.
        
        Args:
            user1: Datos del primer usuario.
            user2: Datos del segundo usuario.
            
        Returns:
            Puntuación de similitud entre los usuarios.
        """
        score = 0.0
        
        # Redes sociales [parametro 4]
        if user1[4] and user2[4]:  # Ambos tienen redes sociales definidas
            score += 0.6
        elif not user1[4] and not user2[4]:  # Ninguno tiene redes sociales definidas
            score += 0.5

        # Edad [parametro 5]
        try:
            # Convierte las fechas de nacimiento a objetos datetime
            fecha_nacimiento1 = datetime.fromisoformat(user1[5])
            fecha_nacimiento2 = datetime.fromisoformat(user2[5])

            # Calcula la diferencia de edad en años decimales
            diferencia_edad = (fecha_nacimiento1-fecha_nacimiento2).days / 365.25

            # Aplica la función exponencial para la similitud de edad
            import numpy as np
            score += 2 * np.exp(-abs(diferencia_edad) / 3)

        except (TypeError, ValueError, IndexError):
            pass  # Ignora si la fecha de nacimiento no es válida o no está presente

        # Género [parametro 6]
        if user1[6] and user2[6] and user1[6] == user2[6]:
            score += 1.0

        # Ocupación [parametro 7]
        if user1[7] and user2[7] and self._compare_string_words(user1[7], user2[7]):
            score += 2.0

        # Deportes [parametro 8]
        if user1[8] and user2[8] and self._compare_string_words(user1[8], user2[8]):
            score += 2.0

        # Presupuesto [parametro 9]
        if abs(user1[9] - user2[9]) < 100:
            score += 1.0

        # Hábitos de limpieza [parametro 10]
        if user1[10] and user2[10] and user1[10] == user2[10]:  # si comparten tipo limpieza
            score += 1.0

        if user1[10] and user2[10] and abs(user1[10]-user2[10]) == 1:  # si son similares
            score += 0.8

        if user1[10] and user2[10] and abs(user1[10]-user2[10]) == 2:  # si difieren por dos
            score += 0.4

        # Horario de trabajo [parametro 11]
        if user1[11] and user2[11] and user1[11] == user2[11]:
            score += 1

        # Mascotas [parametro 12:tiene_mascota] [parametro 13:acepta_mascota]
        if user1[12] and not user2[13]:  # user1 tiene mascota y user2 no la acepta
            score -= 2.0
        if user2[12] and not user1[13]:  # user2 tiene mascota y user1 no la acepta
            score -= 2.0
        if user1[13] and user2[12]:  # user1 acepta mascota y user2 tiene una
            score += 0.5
        if user2[13] and user1[12]:  # user2 acepta mascota y user1 tiene una
            score += 0.5
        if user1[13] == user2[13]:  # Comparten gusto por mascota
            score += 1.0

        # Fumador [parametro 14:es_fumador] [parametro 15:acepta_fumador]
        if user1[14] and not user2[15]:  # user1 fuma y user2 no lo acepta
            score -= 2.0
        if user2[14] and not user1[15]:  # user2 fuma y user1 no lo acepta
            score -= 2.0
        if user1[15] and user2[14]:  # user1 acepta fumador y user2 fuma
            score += 0.5
        if user2[15] and user1[14]:  # user2 acepta fumador y user1 fuma
            score += 0.5
        if user1[15] == user2[15]:  # Comparten gusto sobre fumar
            score += 1.0

        # Intereses [parametro 16]
        try:
            intereses1 = json.loads(user1[16]) if user1[16] else []  # Si user1[16] es None o una cadena vacía, inicializar intereses1 como una lista vacía.
            intereses2 = json.loads(user2[16]) if user2[16] else []  # Lo mismo para intereses2

            if intereses1 and intereses2 and self._compare_string_words(intereses1, intereses2):
                score += 2.0
        except (json.JSONDecodeError, TypeError):
            pass  # Ignora si los intereses no son un JSON válido o si no están presentes

        # Preferencias de roommate [parametro 17]
        try:
            preferencias1 = json.loads(user1[17]) if user1[17] else {}
            preferencias2 = json.loads(user2[17]) if user2[17] else {}

            if preferencias1 and preferencias2 and self._compare_string_words(preferencias1, preferencias2):
                score += 2.0
        except (json.JSONDecodeError, TypeError):
            pass  # Ignora si las preferencias no son un JSON válido o si no están presentes

        return score
    
    def _compare_string_words(self, str1: Union[str, list, dict], str2: Union[str, list, dict]) -> bool:
        """
        Compara dos cadenas de texto (o listas/diccionarios) y busca palabras en común.
        
        Args:
            str1: Primera cadena, lista o diccionario.
            str2: Segunda cadena, lista o diccionario.
            
        Returns:
            True si hay al menos una palabra en común, False en caso contrario.
        """
        import re
        
        def _extract_words(data):
            """Extrae palabras de una cadena, lista o diccionario."""
            if isinstance(data, str):
                return re.findall(r'\b\w+\b', data.lower())
            elif isinstance(data, list):
                return re.findall(r'\b\w+\b', ", ".join(str(x) for x in data).lower())
            elif isinstance(data, dict):
                words = []
                for value in data.values():
                    if isinstance(value, str):
                        words.extend(re.findall(r'\b\w+\b', value.lower()))
                    elif isinstance(value, list):
                        words.extend(re.findall(r'\b\w+\b', ", ".join(str(x) for x in value).lower()))
                return words
            else:
                return []

        palabras1 = _extract_words(str1)
        palabras2 = _extract_words(str2)

        # Buscar palabras en común
        palabras_comunes = set(palabras1) & set(palabras2)

        # Si hay al menos una palabra en común, retornar True
        return len(palabras_comunes) > 0
    
    def calculate_all_similarities(self) -> int:
        """
        Calcula y guarda las similitudes entre todos los pares de usuarios activos.
        
        Returns:
            Número de similitudes calculadas.
        """
        # Obtener los usuarios activos
        usuarios_activos = self.get_active_users()
        count = 0
        
        # Calcular la similitud entre todos los pares de usuarios
        for i in range(len(usuarios_activos)):
            for j in range(i + 1, len(usuarios_activos)):
                user1 = usuarios_activos[i]
                user2 = usuarios_activos[j]
                score = self.calculate_similarity(user1, user2)
                
                # Guardar la similitud
                self.insert_similarity(user1[0], user2[0], score)
                count += 1
        self.commit()
        
        return count

    def commit(self):
        try:
            self.conn.commit()
        except (TypeError, ValueError, IndexError):
            pass
