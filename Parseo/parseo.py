import fitz  # PyMuPDF
import os
import re
from unicodedata import normalize

#Clase para representar una línea de texto con su número de línea
class Linea:
    def __init__(self, numero, texto):
        self.numero = numero
        self.texto = texto

    def __repr__(self):
        return f"{self.numero}: {self.texto}"

    def __str__(self):
        return f"{self.numero}: {self.texto}"

#Funciones de procesamiento de texto

def lineas_repetidas(lineas):
    """Elimina líneas repetidas consecutivas y reacomoda los índices."""
    if not lineas:
        return []
    unicas = [lineas[0]]
    for i in range(1, len(lineas)):
        if lineas[i].texto != lineas[i-1].texto:
            unicas.append(lineas[i])
    acomodar_indices(unicas)
    return unicas

def eliminar_repetidos(lista):
    """Elimina elementos duplicados consecutivos en una lista."""
    if not lista:
        return []
    unicas = [lista[0]]
    for i in range(1, len(lista)):
        if lista[i] != lista[i-1]:
            unicas.append(lista[i])
    return unicas

def acomodar_indices(lineas):
    for i, linea in enumerate(lineas):
        linea.numero = i
    return lineas

def normalizar_texto(texto):
    texto = texto.lower()
    texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1",
        normalize("NFD", texto), 0, re.I
    )
    texto = re.sub(r"\s*\$", "", texto)
    return texto

def encontrar_importes(linea):
    a = -1
    patrones = {
        1: re.compile(r"importe", re.IGNORECASE),
        2: re.compile(r"iva\s*\d+", re.IGNORECASE),
        3: re.compile(r"unidades", re.IGNORECASE),
    }
    texto = linea.texto.lower()
    for codigo, regex in patrones.items():
        if regex.search(texto):
            return codigo
    return a

def buscar_importes(lineas):
    resultados = []
    for i, linea in enumerate(lineas):
        resultadoBusqueda = encontrar_importes(linea)
        if resultadoBusqueda == -1:
            continue
        if resultadoBusqueda == 1:  # Importe
            if i + 1 < len(lineas):
                razon = linea.texto.replace("importe ", "").replace(" $", "")
                monto = lineas[i+1].texto.replace(" $", "")
                resultados.append({"Importe": razon, "Monto": monto})
        elif resultadoBusqueda == 2:  # IVA
            if i + 1 < len(lineas):
                razon = linea.texto.replace("iva ", "").replace(" $", "")
                monto = lineas[i+1].texto.replace(" $", "")
                resultados.append({"IVA": razon, "Monto": monto})
        elif resultadoBusqueda == 3:  # Artículos
            if i >= 2 and i + 5 < len(lineas):
                producto = lineas[i-2].texto
                cantidad = lineas[i-1].texto
                precioUnitario = lineas[i+1].texto
                subtotal = lineas[i+3].texto
                totaliva = lineas[i+5].texto
                resultados.append({
                    "Articulo": producto,
                    "Cantidad": cantidad,
                    "Precio_Unitario": precioUnitario,
                    "Subtotal": subtotal,
                    "TotalIVA": totaliva
                })
    resultados = eliminar_repetidos(resultados)
    return resultados

#Función principal para abrir y procesar el PDF

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

def main_parsear(nombre_archivo):
    print("¿Qué desea procesar?")
    print("1. Solo la factura original (primera página válida)")
    print("2. Todas las páginas válidas")
    try:
        modo = int(input("Ingrese 1 o 2: "))
        if modo not in [1, 2]:
            print("Opción inválida, se usará 'todas las páginas'")
            modo = 2
    except Exception:
        print("Entrada inválida, se usará 'todas las páginas'")
        modo = 2

    resultado = abrirPDF(nombre_archivo, modo)
    if not resultado:
        print("No se encontraron resultados o hubo un error al procesar el PDF.")
        return
    print(*resultado, sep="\n")


if __name__ == "__main__":
    main_parsear()

