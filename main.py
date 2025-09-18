from funciones import buscar_importes, lineas_repetidas, normalizar_texto, buscar_articulos
import fitz  # PyMuPDF
import os
import re
from claseLinea import Linea

    
def main():
    nombre_archivo = input("Ingrese el nombre del archivo PDF (con extensión .pdf): ")
    
    if not os.path.isfile(nombre_archivo):
        print(f"El archivo '{nombre_archivo}' no existe en el directorio actual.")
        return

    try:
        documento = fitz.open(nombre_archivo)
    except Exception as e:
        print(f"No se pudo abrir el archivo PDF: {e}")
        return

    lineas= []

    texto_completo = ""
    for pagina in documento:
        texto_completo += normalizar_texto(pagina.get_text())
        
    
    i=0
    for linea in texto_completo.split('\n'):
        Linea.text = linea.strip()
        Linea.numero = i
        lineas.append(Linea(i, linea.strip()))
        i += 1

    documento.close()
    lineas = lineas_repetidas(lineas)

    resultadoImportes = buscar_importes(lineas)

    print(resultadoImportes)

    resultadoArticulos = buscar_articulos(lineas)
    print(resultadoArticulos)
main()
