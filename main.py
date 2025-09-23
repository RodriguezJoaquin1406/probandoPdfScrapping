from Parseo.parseo import main_parsear
from ConexionesAPi.apiGmail import main_correos

#main_parsear()
file_dir = main_correos()
print(file_dir)
main_parsear(file_dir)