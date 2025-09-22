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
from funciones import get_header, download_attachments


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
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
        print( str(i) + ' ' + title)
    
    while True: 
        try:
            entrada_usuario = input("Ingrese numero del correo a procesar: ")
            eleccion = int(entrada_usuario)
            break  
        except ValueError:
            print("Entrada no válida. Por favor, introduce solo números enteros.")

    archivo = download_attachments(facturas[eleccion], service)

    
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()


