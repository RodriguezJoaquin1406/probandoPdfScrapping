"""
Manejador centralizado de credenciales para APIs externas.
"""
import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class CredentialsManager:
    """
    Manejador centralizado para todas las credenciales del proyecto.
    Utiliza variables de entorno para valores sensibles y proporciona
    una interfaz unificada para acceder a las credenciales.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Inicializa el manejador de credenciales.
        
        Args:
            config_dir: Directorio donde se encuentran los archivos de configuración.
                       Si es None, usa el directorio actual.
        """
        self.config_dir = config_dir or os.path.dirname(__file__)
        self.env_file = os.path.join(self.config_dir, '.env')
        
        # Cargar variables de entorno
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
    
    def get_gmail_scopes(self) -> list:
        """
        Obtiene los scopes de Gmail desde variables de entorno o valores por defecto.
        
        Returns:
            Lista de scopes para la API de Gmail
        """
        default_scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        scopes_env = os.getenv('GMAIL_SCOPES')
        
        if scopes_env:
            return scopes_env.split(',')
        return default_scopes
    
    def get_gmail_credentials_path(self) -> str:
        """
        Obtiene la ruta del archivo de credenciales de Gmail.
        
        Returns:
            Ruta al archivo credentials.json
        """
        credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH')
        if credentials_path:
            return credentials_path
        
        # Buscar en el directorio de configuración o en el directorio raíz del proyecto
        possible_paths = [
            os.path.join(self.config_dir, 'credentials.json'),
            os.path.join(os.path.dirname(self.config_dir), 'credentials.json')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Valor por defecto
        return "credentials.json"
    
    def get_gmail_token_path(self) -> str:
        """
        Obtiene la ruta del archivo de token de Gmail.
        
        Returns:
            Ruta al archivo token.json
        """
        token_path = os.getenv('GMAIL_TOKEN_PATH')
        if token_path:
            return token_path
        
        # Buscar en el directorio de configuración o en el directorio raíz del proyecto
        possible_paths = [
            os.path.join(self.config_dir, 'token.json'),
            os.path.join(os.path.dirname(self.config_dir), 'token.json')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Valor por defecto
        return "token.json"
    
    def get_gmail_credentials(self) -> Optional[Credentials]:
        """
        Obtiene las credenciales autenticadas para Gmail.
        
        Returns:
            Objeto Credentials autenticado para Gmail API
        
        Raises:
            FileNotFoundError: Si no se encuentra el archivo de credenciales
            Exception: Si hay errores en la autenticación
        """
        creds = None
        scopes = self.get_gmail_scopes()
        token_path = self.get_gmail_token_path()
        credentials_path = self.get_gmail_credentials_path()
        
        # El archivo token.json almacena los tokens de acceso y actualización del usuario
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)
        
        # Si no hay credenciales válidas disponibles, permite al usuario iniciar sesión
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error al actualizar credenciales: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(
                        f"Archivo de credenciales no encontrado: {credentials_path}\n"
                        f"Por favor, descarga las credenciales de Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
                creds = flow.run_local_server(port=0)
            
            # Guardar las credenciales para la próxima ejecución
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        
        return creds
    
    def get_gmail_query_sender(self) -> str:
        """
        Obtiene el remitente por defecto para las consultas de Gmail.
        
        Returns:
            Email del remitente configurado
        """
        return os.getenv('GMAIL_DEFAULT_SENDER', 'ertsyvler@gmail.com')
    
    def validate_credentials(self) -> Dict[str, bool]:
        """
        Valida que todas las credenciales necesarias estén disponibles.
        
        Returns:
            Diccionario con el estado de validación de cada servicio
        """
        validation_results = {}
        
        # Validar Gmail
        try:
            gmail_creds = self.get_gmail_credentials()
            validation_results['gmail'] = gmail_creds is not None and gmail_creds.valid
        except Exception as e:
            validation_results['gmail'] = False
            validation_results['gmail_error'] = str(e)
        
        return validation_results
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración desde variables de entorno.
        
        Args:
            key: Clave de la configuración
            default: Valor por defecto si no se encuentra la clave
        
        Returns:
            Valor de la configuración
        """
        return os.getenv(key, default)