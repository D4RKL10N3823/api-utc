"""
Router para autenticación
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import AuthService
from services.usuario_service import UsuarioService
from schemas.usuario import UsuarioLogin, UsuarioCreate, UsuarioResponse, Token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint de registro de usuarios.
    Crea un nuevo usuario en el sistema (público, no requiere autenticación).
    """
    return UsuarioService.create_usuario(db, usuario_data)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login compatible con OAuth2 (Swagger Authorize).
    
    - **username**: Matrícula del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT para usar en las peticiones autenticadas.
    """
    # Convertir form_data a UsuarioLogin
    login_data = UsuarioLogin(
        matricula=form_data.username,  # username = matrícula
        password=form_data.password
    )
    return AuthService.authenticate_user(db, login_data)
