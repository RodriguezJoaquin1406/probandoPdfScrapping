## Api para gmail
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io
import base64
import re
import email
from email import policy
from email.parser import BytesParser
from typing import List, Tuple
import base64

# Importar el manejador de credenciales
from config import CredentialsManager

def get_plain_body(msg):
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body'].get('data')
            if data:
                decoded_bytes = base64.urlsafe_b64decode(data)
                return decoded_bytes.decode('utf-8')
    # Si no hay partes, puede que el cuerpo esté directo
    data = msg['payload']['body'].get('data')
    if data:
        decoded_bytes = base64.urlsafe_b64decode(data)
        return decoded_bytes.decode('utf-8')
    return ""

def mail_has_attachments(msg):
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part.get('filename'):
            return True
    return False


# Fucion para extraer y mostrar los encabezados de un mensaje de Gmail
# Puedo mandarle el nombre del encabezado que quiero extraer
# Ejemplo: get_header(msg, 'Subject') para obtener el asunto
#          get_header(msg, 'From') para obtener el remitente

def get_header(msg, header_name):
    for header in msg['payload']['headers']:
        if header['name'].lower() == header_name.lower():
            return header['value']
    return None
        

#Funcion para descargar los archivos adjuntos de un mensaje de Gmail
# msg: mensaje de Gmail
# service: servicio de Gmail autenticado
# save_dir: donde se guardarán los archivos adjuntos (por defecto carpeta actual)
def download_attachments(msg, service, save_dir='.'):
    parts = msg['payload'].get('parts', [])
    for part in parts:
        filename = part.get('filename')
        if filename and part['body'].get('attachmentId'):
            attachment_id = part['body']['attachmentId']
            att = service.users().messages().attachments().get(
                userId="me", messageId=msg['id'], id=attachment_id
            ).execute()
            data = att['data']
            file_data = base64.urlsafe_b64decode(data)
            with open(f"{save_dir}/{filename}", 'wb') as f:
                f.write(file_data)
            print(f"Descargado: {filename}")
    return filename

def main_correos():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  # Inicializar el manejador de credenciales
  credentials_manager = CredentialsManager()
  
  try:
    # Obtener credenciales usando el manejador centralizado
    creds = credentials_manager.get_gmail_credentials()
    
    if not creds:
      print("No se pudieron obtener las credenciales de Gmail")
      return None

    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()

    facturas = []

    # Get mails from a specific sender using configured sender
    sender = credentials_manager.get_gmail_query_sender()
    query = f"from:{sender}"
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    print(f"Messages  {query}:")
    for message in messages:
      msg = service.users().messages().get(userId="me", id=message["id"]).execute()
      titulo = get_header(msg, 'Subject')
      if titulo and 'factura' in titulo.lower():
        facturas.append(msg)

    if not messages:
      print("No messages found {query}:" )
      return
    
    i = 0
    for i,factura in enumerate(facturas):
        title = get_header(factura, 'Subject') 
        date = get_header(factura, 'Date')
        fecha = date.split(',')[1].strip().split(' ')[0:4]
        fecha = ' '.join(fecha)
        print( str(i) + ' ' + title + ' ' + fecha)
    
    while True: 
        try:
            entrada_usuario = input("Ingrese numero del correo a procesar: ")
            eleccion = int(entrada_usuario)
            if 0 <= eleccion < len(facturas):
              break  
            else:
              print(f"Por favor, ingrese un número entre 0 y {len(facturas)-1}.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce solo números enteros.")

    archivo = download_attachments(facturas[eleccion], service)

    
    return archivo
  
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")
  except Exception as error:
    # Handle other errors (like credential errors)
    print(f"An error occurred: {error}")
    return None


if __name__ == "__main__":
  main_correos()


