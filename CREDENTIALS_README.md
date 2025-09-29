# Sistema de Credenciales Centralizado

Este documento describe el nuevo sistema de manejo de credenciales implementado en el proyecto.

## Estructura del Proyecto

```
probandoPDFscrapping/
├── config/
│   ├── __init__.py
│   ├── credentials_manager.py  # Manejador centralizado de credenciales
│   └── .env                    # Plantilla de variables de entorno
├── ConexionesApi/
│   ├── __init__.py
│   ├── apiGmail.py            # Refactorizada para usar credenciales centralizadas
│   └── apiSheets.py           # Nueva API con sistema modular
└── demo_credentials.py        # Demostración del nuevo sistema
```

## Características Principales

### 🔐 Gestión Centralizada de Credenciales
- Todas las credenciales se manejan desde una única clase `CredentialsManager`
- Configuración a través de variables de entorno
- Validación automática de credenciales disponibles

### 🛡️ Seguridad Mejorada
- Las credenciales sensibles se almacenan en variables de entorno
- Archivos de credenciales excluidos del control de versiones
- Manejo seguro de tokens de autenticación

### 🔧 Configuración Flexible
- Fácil personalización por entorno (desarrollo, producción)
- Valores por defecto sensatos
- Configuración sin código hardcodeado

### 📦 Arquitectura Modular
- Fácil extensión para nuevos servicios de API
- Interfaz unificada para todas las credenciales
- Manejo centralizado de errores

## Uso del Sistema

### Configuración Inicial

1. **Copiar el archivo de configuración:**
   ```bash
   cp config/.env config/.env.local
   ```

2. **Configurar variables de entorno en `.env.local`:**
   ```bash
   # Configuración de Gmail API
   GMAIL_CREDENTIALS_PATH=credentials.json
   GMAIL_TOKEN_PATH=token.json
   GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly
   GMAIL_DEFAULT_SENDER=tu-email@gmail.com
   ```

3. **Descargar credenciales de Google Cloud Console:**
   - Ir a [Google Cloud Console](https://console.cloud.google.com/)
   - Crear/seleccionar proyecto
   - Habilitar Gmail API
   - Crear credenciales OAuth 2.0
   - Descargar como `credentials.json`

### Uso en el Código

#### Gmail API (Refactorizada)
```python
from ConexionesAPi import main_correos

# La función ahora usa automáticamente el sistema centralizado
archivo = main_correos()
```

#### Google Sheets API (Nueva)
```python
from ConexionesAPi import SheetsManager

# Crear instancia del manejador
sheets = SheetsManager()

# Crear nueva hoja
spreadsheet_id = sheets.create_spreadsheet("Mi Hoja")

# Escribir datos
data = [['Columna 1', 'Columna 2'], ['Valor 1', 'Valor 2']]
sheets.write_data(spreadsheet_id, 'A1:B2', data)
```

#### Acceso Directo al Manejador
```python
from config import CredentialsManager

# Inicializar
cm = CredentialsManager()

# Obtener configuraciones
scopes = cm.get_gmail_scopes()
sender = cm.get_gmail_query_sender()

# Validar credenciales
validation = cm.validate_credentials()
if validation['gmail']:
    print("Gmail está configurado correctamente")
```

## Variables de Entorno Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `GMAIL_CREDENTIALS_PATH` | Ruta al archivo credentials.json | `credentials.json` |
| `GMAIL_TOKEN_PATH` | Ruta al archivo token.json | `token.json` |
| `GMAIL_SCOPES` | Scopes de Gmail (separados por coma) | `https://www.googleapis.com/auth/gmail.readonly` |
| `GMAIL_DEFAULT_SENDER` | Email del remitente por defecto | `ertsyvler@gmail.com` |

## Beneficios de la Migración

### Antes (Sistema Anterior)
- ❌ Credenciales hardcodeadas en el código
- ❌ Configuración dispersa en múltiples archivos
- ❌ Difícil mantenimiento y extensión
- ❌ Manejo de errores básico

### Después (Sistema Actual)
- ✅ Credenciales centralizadas y configurables
- ✅ Uso de variables de entorno para seguridad
- ✅ Arquitectura modular y extensible
- ✅ Validación automática y manejo robusto de errores
- ✅ Fácil configuración por entorno
- ✅ Compatible con el código existente

## Troubleshooting

### Error: "Archivo de credenciales no encontrado"
```python
# Verificar que el archivo existe en la ruta especificada
cm = CredentialsManager()
print(f"Buscando credenciales en: {cm.get_gmail_credentials_path()}")
```

### Error: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Configurar múltiples entornos
```bash
# Desarrollo
export GMAIL_DEFAULT_SENDER=dev@example.com

# Producción  
export GMAIL_DEFAULT_SENDER=prod@example.com
```

## Demostración

Ejecutar el script de demostración para ver el sistema en acción:

```bash
python demo_credentials.py
```

Este script muestra:
- Inicialización del sistema
- Carga de configuraciones
- Uso de variables de entorno
- Validación de credenciales
- Integración con APIs existentes

## Próximas Mejoras

- [ ] Soporte para más servicios de Google (Drive, Calendar)
- [ ] Integración con servicios de secrets management
- [ ] Configuración por archivo JSON además de variables de entorno
- [ ] Logging de acceso a credenciales para auditoría
- [ ] Rotación automática de tokens