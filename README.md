# API Hackathon UTC

API REST desarrollada con FastAPI para la gestión de vacantes y usuarios.

## Estructura del Proyecto

```
api-utc/
├── main.py                 # Aplicación principal FastAPI
├── database.py            # Configuración de SQLAlchemy
├── dependencies.py        # Dependencies para FastAPI
├── models/               # Modelos de SQLAlchemy
│   ├── vacante.py
│   └── usuario.py
├── schemas/              # Schemas de Pydantic
│   ├── vacante.py
│   └── usuario.py
├── dao/                  # Data Access Objects (operaciones DB)
│   ├── vacante_dao.py
│   └── usuario_dao.py
├── services/             # Lógica de negocio
│   ├── vacante_service.py
│   ├── usuario_service.py
│   └── auth_service.py
├── routers/              # Endpoints FastAPI
│   ├── vacante_router.py
│   ├── usuario_router.py
│   └── auth_router.py
└── utils/                # Utilidades
    └── security.py       # Funciones de seguridad y JWT
```

## Arquitectura

La aplicación sigue una arquitectura en capas:

1. **Router**: Define los endpoints HTTP y valida las peticiones
2. **Service**: Contiene la lógica de negocio y orquesta las operaciones
3. **DAO**: Realiza las operaciones directas con la base de datos
4. **Models**: Define la estructura de las tablas en la base de datos
5. **Schemas**: Define la estructura de las peticiones/respuestas API

## Instalación

### Prerrequisitos

- Python 3.13+
- PostgreSQL 12+
- Poetry (opcional) o pip

### Paso 1: Instalar dependencias

```bash
# Instalar psycopg2 para PostgreSQL
pip install psycopg2-binary pydantic python-multipart

# O si usas poetry
poetry add psycopg2-binary pydantic python-multipart
```

### Paso 2: Configurar la base de datos

1. Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE hackathon_utc;
```

2. Configurar las variables de entorno:

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
```

3. Ejecutar el script SQL para crear las tablas:

```bash
psql -U postgres -d hackathon_utc -f tabla.sql
```

### Paso 3: Ejecutar la aplicación

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## Documentación API

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Autenticación

- `POST /auth/login` - Login de usuario (retorna JWT token)

### Usuarios

- `POST /usuarios/` - Crear usuario (registro público)
- `GET /usuarios/me` - Obtener usuario actual (requiere token)
- `GET /usuarios/` - Listar usuarios (requiere token)
- `GET /usuarios/{id}` - Obtener usuario por ID (requiere token)
- `PUT /usuarios/{id}` - Actualizar usuario (requiere token)
- `DELETE /usuarios/{id}` - Eliminar usuario (requiere token)

### Vacantes

- `GET /vacantes/` - Listar vacantes (requiere token)
- `GET /vacantes/{id}` - Obtener vacante por ID (requiere token)
- `GET /vacantes/search?empresa=nombre` - Buscar por empresa (requiere token)
- `POST /vacantes/` - Crear vacante (requiere token)
- `PUT /vacantes/{id}` - Actualizar vacante (requiere token)
- `DELETE /vacantes/{id}` - Eliminar vacante (requiere token)

## Autenticación

La API usa JWT (JSON Web Tokens) para autenticación.

### Flujo de autenticación:

1. **Registro**: `POST /usuarios/` con los datos del usuario
2. **Login**: `POST /auth/login` con matrícula y contraseña
3. **Usar token**: Incluir el token en el header `Authorization: Bearer <token>`

### Ejemplo de uso:

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellidos": "Pérez",
    "matricula": "2024001",
    "password": "password123",
    "carrera": "Ingeniería en Sistemas",
    "cuatrimestre": 5
  }'

# 2. Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "matricula": "2024001",
    "password": "password123"
  }'

# Respuesta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }

# 3. Usar el token para acceder a endpoints protegidos
curl -X GET "http://localhost:8000/usuarios/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Conexión a Base de Datos

La conexión a la base de datos se maneja mediante un patrón de **Dependency Injection**:

1. `database.py` crea una única instancia del engine y sessionmaker
2. La función `get_db()` proporciona una sesión que se pasa como parámetro
3. Los DAOs reciben la sesión como argumento, no crean conexiones propias
4. FastAPI gestiona automáticamente el ciclo de vida de la sesión

```python
# Ejemplo de uso en un DAO
@staticmethod
def get_by_id(db: Session, vacante_id: int) -> Optional[Vacante]:
    return db.query(Vacante).filter(Vacante.id == vacante_id).first()

# Ejemplo de uso en un router
@router.get("/{vacante_id}")
def get_vacante(
    vacante_id: int,
    db: Session = Depends(get_db)  # Dependency injection
):
    return VacanteService.get_vacante_by_id(db, vacante_id)
```

## Seguridad

- **Passwords**: Se hashean usando Argon2 (más seguro que bcrypt)
- **JWT**: Tokens con expiración configurable (30 minutos por defecto)
- **CORS**: Configurado para desarrollo (ajustar en producción)

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql://postgres:postgres@localhost:5432/hackathon_utc` |
| `SECRET_KEY` | Clave secreta para JWT | (debe configurarse) |
| `ALGORITHM` | Algoritmo de JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token | `30` |

## Desarrollo

### Ejecutar en modo desarrollo

```bash
uvicorn main:app --reload
```

### Crear migraciones (opcional con Alembic)

```bash
# Instalar alembic
pip install alembic

# Inicializar
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Initial migration"

# Aplicar migración
alembic upgrade head
```

## Producción

Para producción, asegúrate de:

1. Cambiar `SECRET_KEY` a un valor seguro y aleatorio
2. Configurar CORS con orígenes específicos
3. Usar HTTPS
4. Configurar variables de entorno de forma segura
5. Deshabilitar `echo=True` en el engine de SQLAlchemy
6. Usar un servidor ASGI de producción como Gunicorn con Uvicorn workers

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Licencia

MIT
