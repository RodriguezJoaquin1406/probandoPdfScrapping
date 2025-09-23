## Api para gmail
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

def already_exists(filename, directory):
    return os.path.isfile(os.path.join(directory, filename))

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main_correos():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()

    facturas = []

    # Get mails from a specific sender
    query = "from:ertsyvler@gmail.com"
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


if __name__ == "__main__":
  main_correos()


