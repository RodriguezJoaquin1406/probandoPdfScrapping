from funciones import buscar_importes, lineas_repetidas, normalizar_texto
import fitz  # PyMuPDF
import os
from claseLinea import Linea

def abrirPDF(nombre_archivo, modo=2):
    """
    modo=1: solo factura original (primera página válida)
    modo=2: todas las páginas válidas
    """
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

    paginas_validas = []
    for pagina in documento:
        texto_pagina = normalizar_texto(pagina.get_text())
        if "duplicado" not in texto_pagina and "triplicado" not in texto_pagina:
            paginas_validas.append(texto_pagina)

    if modo == 1:
        # Solo la primera página válida (original)
        if paginas_validas:
            texto_completo = paginas_validas[0]
    else:
        # Todas las páginas válidas
        texto_completo = "".join(paginas_validas)

    for i, linea in enumerate(texto_completo.split('\n')):
        if linea.strip():  # Omitir líneas vacías
            lineas.append(Linea(i, linea.strip()))

    documento.close()
    lineas = lineas_repetidas(lineas)
    resultadoImportes = buscar_importes(lineas)
    return resultadoImportes