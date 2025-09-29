"""
API para Google Sheets
Utiliza el manejador centralizado de credenciales.
"""
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any, Optional

# Importar el manejador de credenciales
from config import CredentialsManager


class SheetsManager:
    """
    Manejador para operaciones con Google Sheets.
    """
    
    def __init__(self):
        """
        Inicializa el manejador de Sheets con credenciales centralizadas.
        """
        self.credentials_manager = CredentialsManager()
        self.service = None
    
    def get_service(self):
        """
        Obtiene el servicio de Google Sheets autenticado.
        
        Returns:
            Servicio de Google Sheets
        """
        if not self.service:
            # Nota: Para Sheets necesitaríamos extender el credentials_manager
            # para manejar scopes de Sheets. Por ahora usamos Gmail credentials.
            creds = self.credentials_manager.get_gmail_credentials()
            if creds:
                self.service = build("sheets", "v4", credentials=creds)
        return self.service
    
    def create_spreadsheet(self, title: str) -> Optional[str]:
        """
        Crea una nueva hoja de cálculo.
        
        Args:
            title: Título de la hoja de cálculo
            
        Returns:
            ID de la hoja de cálculo creada o None si hay error
        """
        try:
            service = self.get_service()
            if not service:
                print("No se pudo obtener el servicio de Sheets")
                return None
            
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            
            spreadsheet = service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()
            
            return spreadsheet.get('spreadsheetId')
            
        except HttpError as error:
            print(f"Error al crear la hoja de cálculo: {error}")
            return None
    
    def write_data(self, spreadsheet_id: str, range_name: str, data: List[List[Any]]) -> bool:
        """
        Escribe datos en una hoja de cálculo.
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            range_name: Rango donde escribir (ej: 'A1:C3')
            data: Datos a escribir
            
        Returns:
            True si se escribieron los datos correctamente, False en caso contrario
        """
        try:
            service = self.get_service()
            if not service:
                print("No se pudo obtener el servicio de Sheets")
                return False
            
            body = {
                'values': data
            }
            
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"{result.get('updatedCells')} celdas actualizadas.")
            return True
            
        except HttpError as error:
            print(f"Error al escribir datos: {error}")
            return False
    
    def read_data(self, spreadsheet_id: str, range_name: str) -> Optional[List[List[Any]]]:
        """
        Lee datos de una hoja de cálculo.
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            range_name: Rango a leer (ej: 'A1:C3')
            
        Returns:
            Datos leídos o None si hay error
        """
        try:
            service = self.get_service()
            if not service:
                print("No se pudo obtener el servicio de Sheets")
                return None
            
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            return values
            
        except HttpError as error:
            print(f"Error al leer datos: {error}")
            return None


def main_sheets_demo():
    """
    Función de demostración para el manejo de Google Sheets.
    """
    sheets_manager = SheetsManager()
    
    # Ejemplo de uso
    print("Demostración de Google Sheets API")
    
    # Crear una nueva hoja
    title = "Facturas Procesadas"
    spreadsheet_id = sheets_manager.create_spreadsheet(title)
    
    if spreadsheet_id:
        print(f"Hoja creada con ID: {spreadsheet_id}")
        
        # Escribir datos de ejemplo
        sample_data = [
            ['Fecha', 'Emisor', 'Monto', 'Archivo'],
            ['2023-09-01', 'Empresa A', '150.00', 'factura1.pdf'],
            ['2023-09-02', 'Empresa B', '275.50', 'factura2.pdf']
        ]
        
        success = sheets_manager.write_data(spreadsheet_id, 'A1:D3', sample_data)
        if success:
            print("Datos escritos correctamente")
        
        # Leer los datos escritos
        read_data = sheets_manager.read_data(spreadsheet_id, 'A1:D3')
        if read_data:
            print("Datos leídos:", read_data)
    
    return spreadsheet_id


if __name__ == "__main__":
    main_sheets_demo()