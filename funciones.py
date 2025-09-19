from claseLinea import Linea
import re
from unicodedata import normalize

def lineas_repetidas(Lineas):
    lineas_unicas = []
    lineas_eliminadas = []

    if not Lineas:
        return lineas_unicas, lineas_eliminadas

    # Siempre guardamos la primera
    lineas_unicas.append(Lineas[0])

    for i in range(1, len(Lineas)):
        linea_actual = Lineas[i]
        linea_anterior = Lineas[i - 1]

        if linea_actual.texto != linea_anterior.texto:
            lineas_unicas.append(linea_actual)
        #else:
            #print(f"Línea repetida eliminada: {linea_actual}")

    # Reacomodar índices (si tenés una función para eso)
    acomodar_indices(lineas_unicas)
    return lineas_unicas

def eliminar_repetidos(lista):
    unicas = []
    unicas = []

    if not lista:
        return lista, unicas

    # Siempre guardamos la primera
    unicas.append(lista[0])

    for i in range(1, len(lista)):
        linea_actual = lista[i]
        linea_anterior = lista[i - 1]

        if linea_actual != linea_anterior:
            unicas.append(linea_actual)
        
    return unicas

def acomodar_indices(Lineas):
    """Reasigna los índices de las líneas en una lista de objetos Linea."""
    for i, linea in enumerate(Lineas):
        linea.numero = i
    return Lineas
    

def normalizar_texto(texto):
    # Minúsculas
    texto = texto.lower()
    texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", texto), 0, re.I
    )

    texto = re.sub(r"\s*\$", "", texto)
    
    return texto

def encontrar_importes(Linea):
    a = -1
    patrones = {
        1: re.compile(r"importe", re.IGNORECASE),
        2: re.compile(r"iva\s*\d+", re.IGNORECASE),
        3: re.compile(r"unidades", re.IGNORECASE),
    }

    texto = Linea.texto.lower()

    for codigo, regex in patrones.items():
        if regex.search(texto):
            a = codigo
            return a

    return a
# 1 entonces encontro linea importe
# 2 Encontro iva
# 3 Encontro Articulos

def buscar_importes(Lineas):
    resultados = []

    for i, linea in enumerate(Lineas):
        resultadoBusqueda = encontrar_importes(linea)

        if resultadoBusqueda == -1:
            continue

        if resultadoBusqueda == 1:  # Importe
            if i + 1 < len(Lineas):
                razon = linea.texto.replace("importe ", "").replace(" $", "")
                monto = Lineas[i+1].texto.replace(" $", "")
                resultados.append({"Importe": razon, "Monto": monto})

        elif resultadoBusqueda == 2:  # IVA
            if i + 1 < len(Lineas):
                razon = linea.texto.replace("iva ", "").replace(" $", "")
                monto = Lineas[i+1].texto.replace(" $", "")
                resultados.append({"IVA": razon, "Monto": monto})

        elif resultadoBusqueda == 3:  # Artículos
            if i >= 2 and i + 5 < len(Lineas):
                producto = Lineas[i-2].texto
                cantidad = Lineas[i-1].texto
                precioUnitario = Lineas[i+1].texto
                subtotal = Lineas[i+3].texto
                totaliva = Lineas[i+5].texto
                resultados.append({
                    "Articulo": producto,
                    "Cantidad": cantidad,
                    "Precio_Unitario": precioUnitario,
                    "Subtotal": subtotal,
                    "TotalIVA": totaliva
                })

    resultados = eliminar_repetidos(resultados)
    return resultados