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
# save_dir: directorio donde se guardarán los archivos adjuntos (por defecto es el directorio actual)
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
    