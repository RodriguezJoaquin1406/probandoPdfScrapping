from funciones import buscar_importes, lineas_repetidas, normalizar_texto
import fitz  # PyMuPDF
import os
from claseLinea import Linea

def abrirPDF(nombre_archivo):
    if not os.path.isfile(nombre_archivo):
        print(f"El archivo '{nombre_archivo}' no existe en el directorio actual.")
        return []

    try:
        documento = fitz.open(nombre_archivo)
    except Exception as e:
        print(f"No se pudo abrir el archivo PDF: {e}")
        return []

    lineas = []
    texto_completo = ""
    for pagina in documento:
        texto_pagina = normalizar_texto(pagina.get_text())
        # Excluir páginas con "duplicado" o "triplicado"
        if "duplicado" not in texto_pagina and "triplicado" not in texto_pagina:
            texto_completo += texto_pagina

    for i, linea in enumerate(texto_completo.split('\n')):
        if linea.strip():  # Omitir líneas vacías
            lineas.append(Linea(i, linea.strip()))

    documento.close()
    lineas = lineas_repetidas(lineas)
    resultadoImportes = buscar_importes(lineas)
    return resultadoImportes