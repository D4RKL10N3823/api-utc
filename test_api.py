"""
Script de prueba rápida de los endpoints
Ejecuta este script después de instalar las dependencias
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(response):
    """Imprime la respuesta formateada"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print("-" * 50)

def test_api():
    """Prueba los endpoints principales"""
    
    print("🚀 Probando API Hackathon UTC\n")
    
    # 1. Health check
    print("1️⃣ Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    
    # 2. Crear usuario
    print("2️⃣ Crear Usuario")
    usuario_data = {
        "nombre": "María",
        "apellidos": "González",
        "matricula": "2024999",
        "password": "secure123",
        "carrera": "Ingeniería Industrial",
        "cuatrimestre": 3
    }
    response = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
    print_response(response)
    
    # 3. Login
    print("3️⃣ Login")
    login_data = {
        "matricula": "2024999",
        "password": "secure123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 4. Obtener usuario actual
        print("4️⃣ Obtener Usuario Actual (con token)")
        response = requests.get(f"{BASE_URL}/usuarios/me", headers=headers)
        print_response(response)
        
        # 5. Crear vacante
        print("5️⃣ Crear Vacante")
        vacante_data = {
            "nombre_empresa": "Google México",
            "datos_vacante": "Software Engineer - Backend Python"
        }
        response = requests.post(f"{BASE_URL}/vacantes/", json=vacante_data, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            vacante_id = response.json()["id"]
            
            # 6. Obtener vacante
            print("6️⃣ Obtener Vacante")
            response = requests.get(f"{BASE_URL}/vacantes/{vacante_id}", headers=headers)
            print_response(response)
            
            # 7. Actualizar vacante
            print("7️⃣ Actualizar Vacante")
            update_data = {
                "datos_vacante": "Software Engineer - Full Stack Python + React"
            }
            response = requests.put(f"{BASE_URL}/vacantes/{vacante_id}", json=update_data, headers=headers)
            print_response(response)
            
            # 8. Listar todas las vacantes
            print("8️⃣ Listar Vacantes")
            response = requests.get(f"{BASE_URL}/vacantes/", headers=headers)
            print_response(response)
        
        print("✅ Todas las pruebas completadas!")
    else:
        print("❌ Error en login, no se pueden ejecutar más pruebas")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API")
        print("Asegúrate de que la API esté ejecutándose:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
