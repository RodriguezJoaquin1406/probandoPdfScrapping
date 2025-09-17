from claseLinea import Linea

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
        else:
            lineas_eliminadas.append(linea_actual)

    # Reacomodar índices (si tenés una función para eso)
    acomodar_indices(lineas_unicas)
    return lineas_eliminadas

def acomodar_indices(Lineas):
    """Reasigna los índices de las líneas en una lista de objetos Linea."""
    for i, linea in enumerate(Lineas):
        linea.numero = i
    return Lineas
    

def limpiar_renglones_repetidos_texto(texto):
    """Elimina renglones repetidos en un bloque de texto."""
    lineas = texto.split('\n')
    lineas_unicas = []
    for linea in lineas:
        linea = linea.strip()
        if linea and linea not in lineas_unicas:
            lineas_unicas.append(linea)
    return '\n'.join(lineas_unicas)