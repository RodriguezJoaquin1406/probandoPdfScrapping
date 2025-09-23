from archivo import abrirPDF

def main():
    nombre_archivo = input("Ingrese nombre archivo PDF (con .pdf): ")
    resultado = abrirPDF(nombre_archivo)
    if not resultado:
        print("No se encontraron resultados o hubo un error al procesar el PDF.")
        return
    print(*resultado, sep="\n")

if __name__ == "__main__":
    main()