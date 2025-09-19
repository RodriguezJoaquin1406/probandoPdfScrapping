from archivo import parsearPDF
    
def main():
    
    nombre_archivo = input("Ingrese nombre archivo PDF (con .pdf): ")
    resultado = parsearPDF(nombre_archivo)
    print(*resultado , sep = "\n")

main()
