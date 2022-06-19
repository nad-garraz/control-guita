import os
import prompts as gp
import funciones as gf

# TODO
# Estaría bueno parsear esto desde una config file en vez de que esté
# hardcodeado así. Y también poder cambiar el archivo de datos desde
# el programa
directorio_local = ".local/guitarra"
directorio_datos = "datos"
directorio_bkp = "bkp"
directorio_cambios = "cambios"
nombre_archivo = "current_nombre"


def get_directorio_local():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea y luego se crea el archivo de datos
    """
    home = os.getenv("HOME")
    local_dir = os.path.join(home, directorio_local)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    return local_dir


def get_directorio_datos():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea.
    """
    datos_dir = os.path.join(get_directorio_local(), directorio_datos)
    if not os.path.isdir(datos_dir):
        os.mkdir(datos_dir)
    return datos_dir


def get_directorio_bkp():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea.
    """
    datos_dir = os.path.join(get_directorio_local(), directorio_bkp)
    if not os.path.isdir(datos_dir):
        os.mkdir(datos_dir)
    return datos_dir


def get_directorio_cambios():
    """
    Se prueba la existencia del directorio. Si no existe
    se crea.
    """
    cambios_dir = os.path.join(get_directorio_local(), directorio_cambios)
    if not os.path.isdir(cambios_dir):
        os.mkdir(cambios_dir)
    return cambios_dir


def get_file_current():
    local_dir = get_directorio_local()
    filename = os.path.join(
        local_dir, nombre_archivo
    )  # Inicializo el archivo que contiene dentro a current_datos
    if not os.path.isfile(
        filename
    ):  # Si no existe el archivo que tiene el nombre lo crea
        gf.touch(filename)
    return filename


def get_current_archivo_datos():
    """
    Se prueba la existencia del archivo. Si no existe
    se crea. Luego se extrae la información que contiene.
    """
    # local_dir = get_directorio_local()
    datos_dir = get_directorio_datos()
    filename = get_file_current()
    if os.stat(filename).st_size == 0:
        current_datos = cambiar_archivo_datos()
    else:
        with open(filename, "r") as current_nombre:
            current_datos_rel_path = current_nombre.read().replace(
                "\n", ""
            )  # Si no el output me sale con un "\n"
        current_datos = os.path.join(datos_dir, current_datos_rel_path)
        if os.path.isfile(current_datos):
            return current_datos
        else:
            gp.separador(1)
            print("¡No hay archivo seleccionado para trabajar!")
            current_datos = cambiar_archivo_datos()


def cambiar_archivo_datos():
    """
    Pasa el nombre del archivo de datos que se quiere usar
    """
    local_dir = get_directorio_local()
    datos_dir = get_directorio_datos()
    gp.separador()
    print("Elegir archivo:")
    list_archivos_datos = [item for item in os.listdir(datos_dir) if item[-3:] == "csv"]
    archivos_dict = {}
    for num, item in enumerate(
        list_archivos_datos, 1
    ):  # Lista enumerada con los archivos de datos
        archivos_dict[str(num)] = item
        print(f"{num}) {item}")
    gp.separador()
    key_current_datos = input("¿Cuál archivo? Elegir número: \n")
    current_datos = archivos_dict[key_current_datos]
    gp.separador()
    filename = os.path.join(local_dir, nombre_archivo)
    with open(filename, "w") as current_nombre:
        current_nombre.write(current_datos)
    current_datos = os.path.join(datos_dir, current_datos)
    os.system("clear")
    return current_datos


def backup_datos(archivo_de_datos):
    """
    Si el archivo de datos no está vacío se hace un backup local
    """
    directorio_bkp = get_directorio_bkp()
    strip_name = (
        archivo_de_datos[0:-4].split("/")[-1] + ".tar.bzip2"
    )  # Saco el último término de archivo_de_datos y le cambio la extensión.
    name_bkp = os.path.join(directorio_bkp, strip_name)
    if not os.path.getsize(archivo_de_datos) == 0:
        os.system(f"tar -cjP {archivo_de_datos} -f {name_bkp}")
