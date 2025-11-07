"""
Script para crear un usuario de prueba
"""
from database import get_db_context
from services.usuario_service import UsuarioService
from schemas.usuario import UsuarioCreate


def create_test_user():
    """Crea un usuario de prueba"""
    with get_db_context() as db:
        usuario_data = UsuarioCreate(
            nombre="Test",
            apellidos="Usuario",
            matricula="TEST001",
            password="test123456",
            carrera="Ingeniería en Sistemas",
            cuatrimestre=5
        )
        
        try:
            usuario = UsuarioService.create_usuario(db, usuario_data)
            print(f"✅ Usuario creado exitosamente:")
            print(f"   ID: {usuario.id}")
            print(f"   Nombre: {usuario.nombre} {usuario.apellidos}")
            print(f"   Matrícula: {usuario.matricula}")
            print(f"   Carrera: {usuario.carrera}")
            print(f"\nPuedes hacer login con:")
            print(f"   Matrícula: {usuario.matricula}")
            print(f"   Password: test123456")
        except Exception as e:
            print(f"❌ Error al crear usuario: {str(e)}")


if __name__ == "__main__":
    create_test_user()
