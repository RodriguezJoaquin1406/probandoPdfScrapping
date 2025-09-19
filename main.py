from funciones import buscar_importes, lineas_repetidas, normalizar_texto
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
        texto_pagina = normalizar_texto(pagina.get_text())
        if(texto_pagina.__contains__("duplicado") == False and texto_pagina.__contains__("triplicado")):
            texto_completo += normalizar_texto(texto_pagina)
    
    i=0
    for linea in texto_completo.split('\n'):
        Linea.text = linea.strip()
        Linea.numero = i
        lineas.append(Linea(i, linea.strip()))
        i += 1

    documento.close()
    lineas = lineas_repetidas(lineas)


    resultadoImportes = buscar_importes(lineas)

    print(*resultadoImportes, sep = "\n")


main()
