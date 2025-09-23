from claseLinea import Linea
import re
from unicodedata import normalize

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