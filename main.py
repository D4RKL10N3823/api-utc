"""
Aplicación principal de FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import vacante_router, usuario_router, auth_router, postulacion_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Hackathon UTC",
    description="API para gestión de vacantes y usuarios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(vacante_router)
app.include_router(postulacion_router)


@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación"""
    # Inicializar la base de datos (crear tablas)
    init_db()


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "API Hackathon UTC",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {"status": "ok"}
