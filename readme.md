# Sistema de Recomendación de Compañeros de Alquiler

Un sistema inteligente para encontrar compañeros de cuarto compatibles basado en perfiles de usuario y algoritmos de similitud.

## 📋 Descripción del Proyecto

Este sistema ayuda a los usuarios a encontrar compañeros de cuarto (roommates) potencialmente compatibles analizando perfiles de usuario y calculando la similitud entre ellos. La plataforma ofrece recomendaciones personalizadas de los 10 usuarios más compatibles para compartir alquiler, facilitando la búsqueda de compañeros de vivienda con intereses y estilos de vida afines.

## 🚀 Características Principales

- **Registro y perfil de usuario**: Captura información relevante como datos personales, preferencias de vivienda, hábitos, intereses y presupuesto.
- **Sistema de recomendación**: Algoritmo que calcula la compatibilidad entre usuarios y sugiere los 10 mejores matches.
- **Dashboard personalizado**: Vista de usuario con recomendaciones actualizadas y opciones de contacto.
- **API REST**: Backend desarrollado en Python para gestionar usuarios y cálculos de similitud.
- **Base de datos segura**: Almacenamiento de perfiles de usuario y matriz de similitud en base de datos relacional.
- **Escalabilidad en la nube**: Preparado para migración a AWS S3 para mayor escalabilidad.

## 🛠️ Arquitectura del Sistema

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    Frontend     │     │    Backend API   │     │   Base de Datos  │
│  (HTML/CSS/JS)  │◄───►│     (Python)     │◄───►│     (MySQL)      │
└─────────────────┘     └──────────────────┘     └──────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │  Algoritmo de    │
                        │   Similitud      │
                        └──────────────────┘
```

## 🔧 Tecnologías Utilizadas

### Frontend
- HTML5, CSS3, JavaScript
- Gestión de estado: Redux

### Backend
- Python 3.9+
- Framework: FastAPI
- ORM: SQLAlchemy
- Cálculo de similitud: Scikit-learn

### Base de Datos
- MySQL (desarrollo local)
- Opción de migración a AWS S3 y DynamoDB

### Herramientas de Desarrollo
- Docker para contenerización
- Pytest para pruebas automatizadas
- GitHub Actions para CI/CD

## 📊 Modelo de Datos

### Tabla de Usuarios
```
- user_id (PK)
- nombre
- email
- teléfono
- edad
- género
- ocupación
- deportes
- presupuesto_máximo
- hábitos_limpieza (1-5)
- horario_trabajo
- mascota (boolean)
- fumador (boolean)
- intereses (JSON)
- preferencias_roommate (JSON)
- fecha_registro
- última_actualización
```

### Matriz de Similitud
```
- user_id_1 (PK)
- user_id_2 (PK)
- score_similitud
- fecha_cálculo
```

## 🔄 Flujo de Trabajo ETL

1. **Extracción**: Recopilación de datos de perfil de usuario.
2. **Transformación**: Procesamiento y vectorización de perfiles para cálculo de similitud.
3. **Carga**: Actualización de la matriz de similitud en la base de datos.
4. **Programación**: Actualización local cada vez que se modifica un usuario (cada usuario puede modificarse maximo 1 vez al dia)

## 🛣️ Roadmap de Desarrollo

### Fase 1: MVP (Producto Mínimo Viable)
- [x] Definición de modelo de datos
- [ ] Implementación de base de datos relacional
- [ ] Desarrollo de API básica CRUD (Create, Read, Update, Delete)
- [ ] Frontend básico de registro y visualización de perfil
- [ ] Algoritmo simple de similitud basado en atributos clave

### Fase 2: Características Principales
- [ ] Sistema completo de autenticación y autorización
- [ ] Dashboard de usuario con recomendaciones
- [ ] Mejora del algoritmo de similitud con ponderaciones personalizables
- [ ] Integración de pruebas automatizadas
- [ ] Implementación de Docker para desarrollo

### Fase 3: Optimización y Escalabilidad
- [ ] Migración opcional a AWS S3 para almacenamiento
- [ ] Implementación de caché para consultas frecuentes
- [ ] Refinamiento del algoritmo con técnicas de machine learning
- [ ] Monitoreo y analítica de uso
- [ ] Optimización de rendimiento

## 🔐 Consideraciones de Seguridad y Privacidad

- Encriptación de datos sensibles (contraseñas, información personal)
- Cumplimiento con regulaciones de protección de datos
- Políticas claras de privacidad y consentimiento de usuario
- Limitación de acceso a información de contacto hasta match mutuo

## 🚀 Instalación y Configuración (Desarrollo Local)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/roommate-recommender.git
cd roommate-recommender

# Configurar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Iniciar la base de datos
python scripts/init_db.py

# Ejecutar el servidor de desarrollo
python app.py
```

## 📝 Contribución

Si deseas contribuir al proyecto, por favor:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`)
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📧 Contacto

Para preguntas o sugerencias, por favor contáctanos en: [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)
