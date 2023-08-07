from datetime import date
import input_manipulation as gim
# import plots as gpl
import prompts as gp
import os
import conversion_dinero as gcd

exit = ["quit", "exit", "q", "5"]


def archivo_a_lista(archivo):
    """
    Saco informacion de un CSV, asociando los 2 primeros renglones a variables,
    luego dejando una lista con solo los datos ingresados
    """
    with open(archivo, mode="r") as extracted_file:
        # lista = [row.rstrip().split(",") for row in extracted_file]
        lista = [row.rstrip().split(",") for row in extracted_file if row[0] != "#"]
        archivo_currency = lista.pop(0)[0]  # Tomo valor y saco elemento
        categorias = lista.pop(0)  # Tomo valor y saco elemento
    return lista, archivo_currency, categorias


def eleccion_usuario():
    """
    TODO -> maybe try, except block??
    """
    opcion_valida = {"1", "2", "3", "4"}.union(set(exit))
    while True:
        eleccion = str(input("Qué querés hacer?: "))
        if eleccion in opcion_valida:
            break
        else:
            print("¡Opción incorrecta! Ingresa una opción válida:")
    gp.separador(1)
    return eleccion


def agregar_dato_a_archivo(fecha, monto, categoria, archivo, valor_dolar):
    """
    writes a line of formated and coma separated values to file
    """
    with open(archivo, mode="a+") as datos_file:
        conversion = gcd.to_dolar2(monto, valor_dolar)
        datos_file.write(f"{fecha},{monto},{conversion},{categoria}\n")


def mostrar_lista_de_entradas(lista):
    """
    Para mostrar los datos en forma legible separando los
    meses con unas rayitas
    """
    fecha_actual = lista[0][0][6]  # primer dígito del mes
    for indice, linea in enumerate(lista, 1):
        fecha, monto, dolar, categoria = linea
        if fecha[6] != fecha_actual:
            fecha_actual = fecha[6]
            gp.separador(1, "-")
        print(f"{indice:<3}{fecha:>12}{monto:>10} {categoria:<}")


def delta_days_abs(lista):
    """
    returns the days that passed between today and the first date of the csv file.
    The file MUST be alphabeticaly sorted
    """
    fecha_objeto1 = date.fromisoformat(lista[0][0])
    today = date.today()
    delta_days = str(today - fecha_objeto1).split(" ")[0]
    return float(delta_days)


def palabras_a_dicc(palabras_csv):
    """
    Paso de una lista de palabras a un diccionario donde
    la primera letra de la palabra es la key y la palabra es el value
    """
    diccionario = {}  # Declaro el diccionario
    for elemento in palabras_csv:
        diccionario[elemento[0].capitalize()] = elemento.capitalize()
    return diccionario


def totales_de_categorias(diccionario, lista):
    """
    Returns a diccionary with the sum of all the elements of the categories in
    the second line of "datos_file" respectely.
    """
    dicc_categoria_totales = {}
    for categoria in diccionario.keys():
        lista_para_una_categoria = []
        for row in lista:
            if row[3][0] == categoria:  # Columna categorias
                lista_para_una_categoria.append(float(row[1]))
        total_de_categoria = round(sum(lista_para_una_categoria), 2)
        dicc_categoria_totales[categoria] = total_de_categoria
    return dicc_categoria_totales


def selector_de_periodo(lista):
    """
    Elegir periodo de fechas para analizar
    """
    # Tomar una fecha inicial
    desde_fecha = input("Fecha inicial: ")
    desde_fecha = gim.recibir_fecha(desde_fecha)
    # Tomar una fecha final
    hasta_fecha = input("Fecha final (hoy): ")
    if hasta_fecha == "":
        hasta_fecha = date.today()
    else:
        hasta_fecha = gim.recibir_fecha(hasta_fecha)
    # Correr analisis para esos datos
    nueva_lista = []
    for row in lista:
        if desde_fecha <= date.fromisoformat(row[0]) <= hasta_fecha:
            nueva_lista.append(row)
    delta_days = str(hasta_fecha - desde_fecha).split(" ")[0]
    return nueva_lista, float(delta_days)


def editar_manual(archivo):
    os.system(f"$EDITOR {archivo}")


def order_first_column_by_dates(archivo):
    """
    A partir de un archivo que tiene sus dos primeras filas con datos no
    relevantes para el orden, se generan 2 listas, una con lineas que
    empiezan con "#" y otra donde las lineas empiezan con una fecha
    "yyyy-mm-dd". Se ordena la segunda y luego se concatenan,
    para finalmente escribir en el mismo archivo del cual se extrajo la
    informacion, las primeras 2 filas + la lista ordenada +
    las lista queempieza con "#"
    """
    with open(archivo, mode="r") as extracted_file:
        lista = []
        lista_commented = []
        for row in extracted_file:
            if row[0] != "#":
                lista.append(row)
            else:
                lista_commented.append(row)
    for i in range(2, len(lista)):
        minimo_fecha = lista[i].split(",")[0]
        minimo_fecha_objeto = date.fromisoformat(minimo_fecha)
        for j in range(i + 1, len(lista)):
            comparar_fecha = lista[j].split(",")[0]
            comparar_fecha_objeto = date.fromisoformat(comparar_fecha)
            if comparar_fecha_objeto < minimo_fecha_objeto:
                nuevo_minimo_lista = lista[j]
                minimo_fecha = lista[j].split(",")[0]
                minimo_fecha_objeto = date.fromisoformat(minimo_fecha)
                lista[j] = lista[i]
                lista[i] = nuevo_minimo_lista
    lista_aumentada = lista + lista_commented
    with open(archivo, mode="w") as f:
        for linea in lista_aumentada:
            f.write(linea)


def touch(path):
    with open(path, "a"):
        os.utime(path, None)
