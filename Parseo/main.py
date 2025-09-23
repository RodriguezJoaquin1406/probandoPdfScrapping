from archivo import abrirPDF

def main():
    nombre_archivo = input("Ingrese nombre archivo PDF (con .pdf): ")
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
    main()