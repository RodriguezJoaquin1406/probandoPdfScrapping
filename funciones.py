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

    return texto

def encontrar_importes(Linea):
    # Cabeceras de interés
    claves = [
        "importe otros tributos: $",
        "importe neto gravado: $" ,
        "iva 27%: $",
        "iva 21%: $",
        "iva 10.5%: $",
        "iva 5%: $",
        "iva 2.5%: $",
        "importe total: $",
        "iva 0%: $"
    ]
    
    texto = Linea.texto

    if texto in claves:
        return True
    else:
        return False

def buscar_importes(Lineas):
    montos = []

    i = 0
    for linea in Lineas:
        if(encontrar_importes(linea) and i > 0):
            razon = Lineas[i].texto.replace(" $", "")
            monto= Lineas[i+1].texto
            if(monto != "0,00"):
                montoDic = dict( razon =  razon, monto = monto)
                montos.append(montoDic) 
        i = i + 1

    return montos

def buscar_articulos(Lineas):
    articulos = []

    i = 0
    for linea in Lineas:
        if(linea.texto == "unidades"):
            producto = Lineas[i-2].texto
            cantidad = Lineas[i-1].texto
            precioUnitario = Lineas[i+1].texto
            subtotal = Lineas[i+3].texto
            totaliva = Lineas[i+5].texto
            articulosDic = dict(Articulo = producto, Cantidad = cantidad, Precio_Unitario = precioUnitario, Subtotal = subtotal, TotalIVA = totaliva)
            articulos.append(articulosDic)
        i = i + 1
    
    return articulos
        