import os


directorio_local = ".local/guitarra"
nombre_archivo = "datos.csv"

def get_directorio_datos():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea y luego se crea el archivo de datos
    """
    home = os.getenv("HOME")
    local_dir = os.path.join(home, directorio_local)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    return local_dir

def get_archivo_datos():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea y luego se crea el archivo de datos
    """
    local_dir = get_directorio_datos()
    filename = os.path.join(local_dir, nombre_archivo)
    if not os.path.isfile(filename):
        os.mknod(filename)
    return filename

def backup_datos(archivo_de_datos):
    """
    Si el archivo de datos no está vacío se hace un backup local
    """
    backup = archivo_de_datos[0:-4] + ".tar.bzip2"
    if not os.path.getsize(archivo_de_datos) == 0:
        os.system(f'tar -cjP {archivo_de_datos} -f {backup}')
