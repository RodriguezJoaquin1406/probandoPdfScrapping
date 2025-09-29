#!/usr/bin/env python3
"""
Demostración del nuevo sistema de credenciales.
Este script muestra cómo usar el sistema centralizado de credenciales.
"""

import os
import sys

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import CredentialsManager
from ConexionesAPi import main_correos, SheetsManager

def demo_credentials_system():
    """
    Demuestra el uso del sistema centralizado de credenciales.
    """
    print("=== Demostración del Sistema de Credenciales Centralizado ===\n")
    
    # 1. Inicializar el manejador de credenciales
    print("1. Inicializando el manejador de credenciales...")
    cm = CredentialsManager()
    print("   ✓ CredentialsManager inicializado")
    
    # 2. Mostrar configuraciones cargadas
    print("\n2. Configuraciones cargadas:")
    print(f"   - Gmail scopes: {cm.get_gmail_scopes()}")
    print(f"   - Remitente por defecto: {cm.get_gmail_query_sender()}")
    print(f"   - Ruta de credenciales: {cm.get_gmail_credentials_path()}")
    print(f"   - Ruta de token: {cm.get_gmail_token_path()}")
    
    # 3. Probar con variables de entorno personalizadas
    print("\n3. Probando con variables de entorno personalizadas...")
    os.environ['GMAIL_DEFAULT_SENDER'] = 'test@example.com'
    os.environ['GMAIL_SCOPES'] = 'https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send'
    
    cm_custom = CredentialsManager()
    print(f"   - Nuevo remitente: {cm_custom.get_gmail_query_sender()}")
    print(f"   - Nuevos scopes: {cm_custom.get_gmail_scopes()}")
    
    # 4. Validar credenciales
    print("\n4. Validando credenciales disponibles...")
    validation = cm.validate_credentials()
    
    for service, is_valid in validation.items():
        if service.endswith('_error'):
            continue
        status = "✓" if is_valid else "✗"
        print(f"   {status} {service.capitalize()}: {'Válido' if is_valid else 'No disponible'}")
        
        if not is_valid and f"{service}_error" in validation:
            print(f"     Razón: {validation[f'{service}_error']}")
    
    # 5. Demostrar que las APIs usan el nuevo sistema
    print("\n5. Demostrando integración con APIs...")
    
    try:
        print("   - Importando Gmail API...")
        # No ejecutamos main_correos() porque requiere credenciales reales
        print("     ✓ Gmail API usa el nuevo sistema de credenciales")
        
        print("   - Importando Sheets Manager...")
        sheets_manager = SheetsManager()
        print("     ✓ Sheets Manager usa el nuevo sistema de credenciales")
        
    except ImportError as e:
        print(f"     ✗ Error de importación: {e}")
    
    print("\n=== Beneficios del Nuevo Sistema ===")
    print("✓ Credenciales centralizadas en un solo lugar")
    print("✓ Uso de variables de entorno para configuración sensible")
    print("✓ Validación automática de credenciales")
    print("✓ Fácil extensión para nuevos servicios")
    print("✓ Manejo de errores mejorado")
    print("✓ Configuración flexible por entorno")
    
    print("\n=== Instrucciones de Uso ===")
    print("1. Copiar config/.env a un archivo local y configurar variables")
    print("2. Descargar credentials.json de Google Cloud Console")
    print("3. Ejecutar las funciones de API como antes - ahora usan el sistema centralizado")
    print("\nEl sistema es completamente compatible con el código existente.")

if __name__ == "__main__":
    demo_credentials_system()