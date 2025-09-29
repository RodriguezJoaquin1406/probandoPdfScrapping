from Parseo.parseo import main_parsear
from ConexionesAPi.apiGmail import main_correos


#file_dir = main_correos()
file_dir = "factura2.pdf"
print(file_dir)
informacionFiltrada = main_parsear(file_dir)
print(informacionFiltrada)
