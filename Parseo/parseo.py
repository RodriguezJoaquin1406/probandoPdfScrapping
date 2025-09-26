from datetime import datetime
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

def buscar_importes(lineas, modo):
    resultados = []
    for i, linea in enumerate(lineas):
        resultadoBusqueda = encontrar_importes(linea)
        if resultadoBusqueda == -1:
            continue
        if resultadoBusqueda == 1 and modo == "importes":  # Importe
            if i + 1 < len(lineas):
                razon = linea.texto.replace("importe ", "").replace(" $", "")
                monto = lineas[i+1].texto.replace(" $", "")
                if monto != "0,00":
                    resultados.append("Importe" + " " + razon + " " + "Monto:" + " " + monto)
        elif resultadoBusqueda == 2 and modo == "importes":  # IVA
            if i + 1 < len(lineas):
                razon = linea.texto.replace("iva ", "").replace(" $", "")
                monto = lineas[i+1].texto.replace(" $", "")
                if monto != "0,00":
                    resultados.append("IVA" + " " + razon + " " + "Monto:" + " " + monto)
        elif resultadoBusqueda == 3 and modo == "articulos":  # Artículos
            if i >= 2 and i + 5 < len(lineas):
                producto = lineas[i-2].texto
                cantidad = lineas[i-1].texto
                precioUnitario = lineas[i+1].texto
                subtotal = lineas[i+3].texto
                totaliva = lineas[i+5].texto
                resultados.append(
                    "Articulo:" + " " +  producto + " " +
                    "Cantidad:" + " " + cantidad + " " +
                    "Precio_Unitario:" + " " + precioUnitario + " " +
                    "Subtotal:" + " " + subtotal + " " +
                    "TotalIVA:" + " " + totaliva
                )
    resultados = eliminar_repetidos(resultados)
    return resultados


def  encontrar_razon_social(linea):
    a = -1
    patrones = {
        1: re.compile(r"original", re.IGNORECASE),
        2: re.compile(r"condicion frente al iva:", re.IGNORECASE),
    }
    texto = linea.texto.lower()
    for codigo, regex in patrones.items():
        if regex.search(texto):
            return codigo
    return a

def buscar_razon_social(lineas):
    resultado= ""
    encontroFactura = False
    for i, linea in enumerate(lineas):
        resultadoBusqueda = encontrar_razon_social(linea)
        if resultadoBusqueda == -1:
            continue
        if resultadoBusqueda == 1:  # Razon Social
            if i + 1 < len(lineas):
                razon = lineas[i+1].texto
                resultado += "razon social:" + " " + razon
        elif resultadoBusqueda == 2:  # Caract Facturas
            if i + 1 < len(lineas):
                if not encontroFactura:
                    fecha = lineas[i+3].texto
                    encontroFactura = True
                    resultado += "fecha:" + " " + fecha
        
                else:
                    if encontroFactura == True:
                        factura = lineas[i+2].texto
                        factura += " "
                        factura += lineas[i-4].texto
                        resultado += "factura:" + " " + factura

    return resultado

def delete_file(filename, directory):
    if __name__ == "__main__":
        return
    
    try:
        os.remove(os.path.join(directory, filename))
        print(f"Eliminado: {filename}")
    except Exception as e:
        print(f"Error al eliminar {filename}: {e}")

def export_to_txt(content, filename, unidades_o_articulos):
    # Filename with date-time to avoid overwriting
    filename = filename.replace("razon social: ", "")
    filename = filename.replace("fecha: ", "")
    filename = filename.replace("factura: ", "")
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "-")
    filename += "_" + unidades_o_articulos
    filename = f"{os.path.splitext(filename)[0]}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Exportado a: {filename}")
    except Exception as e:
        print(f"Error al exportar a {filename}: {e}")

def export_to_csv(content, filename):
    # Filename with date-time to avoid overwriting
    filename = filename.replace("razon social: ", "")
    filename = filename.replace("fecha: ", "")
    filename = filename.replace("factura: ", "")
    filename = filename.replace(" ", "_")
    filename = filename.replace("/", "-")
    filename += "_importes"
    filename = f"{os.path.splitext(filename)[0]}.csv"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Exportado a: {filename}")
    except Exception as e:
        print(f"Error al exportar a {filename}: {e}")

#Función principal para abrir y procesar el PDF

def abrirPDF(nombre_archivo, modo=2):
    resultadoImportes = []
    resultadoArticulos = []
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
    titulo = buscar_razon_social(lineas)
    resultadoImportes = buscar_importes(lineas, "importes")
    export_to_txt(str(resultadoImportes), titulo , "importes" )
    resultadoArticulos = buscar_importes(lineas, "articulos")
    export_to_txt(str(resultadoArticulos), titulo , "articulos" )
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

    delete_file(nombre_archivo, ".")
    if not resultado:
        print("No se encontraron resultados o hubo un error al procesar el PDF.")
        return
    print(*resultado, sep="\n")


if __name__ == "__main__":
    try:
        nombre_archivo = input("Ingrese nombre archivo: ")
        main_parsear(nombre_archivo)
    except Exception as e:
        print(f"Error en la ejecución: {e}")
