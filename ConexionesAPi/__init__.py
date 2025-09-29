"""
Módulo de conexiones a APIs externas.
Utiliza el sistema centralizado de credenciales para autenticación.
"""

from .apiGmail import main_correos
from .apiSheets import SheetsManager, main_sheets_demo

__all__ = ['main_correos', 'SheetsManager', 'main_sheets_demo']