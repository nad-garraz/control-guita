import plots as gpl
import funciones as gf

# import input_manipulation as gim


def separador(lineas=1, simbolo="="):
    """asteriscs for decoration"""
    linea_separadora = simbolo * 55
    for linea in range(lineas):
        print(f"{linea_separadora}")


def intro_current_datos(archivo_de_datos, archivo_currency, categorias):
    separador(1)
    paises_dict = {
        "usa": "USA",
        "eur": "Europa",
        "arg": "Argentina",
        "nz": "New Zealand",
    }
    pais = archivo_de_datos.split("_")[1]
    print(f"Lugar: {paises_dict[pais]}")
    print(f"Moneda: {archivo_currency}")


def principal_menu():
    separador(1)
    menu_dict = {
        "1": "Ingresar movimiento",
        "2": "Info monetaria",
        "3": "Corregir datos manualmente",
        "4": "Cambiar archivo de datos",
        "5": "Salir",
    }
    for key, value in menu_dict.items():
        print(f"{key} - {value}")
    separador()


def option_two_menu():
    """Presents the data after asking for the period or
    dates to analize"""
    separador(1)
    menu_dict = {
        "1": "Toda la lista",
        "2": "Intervalo especial",
        "3": "Pie gastos",
        "4": "Historial del ahorro",
    }
    for k, v in menu_dict.items():
        print(f"{k} - {v}")
    separador(1)


def prompt_data(eleccion, lista_de_datos, archivo_currency, categorias, valor_dolar):
    categoria_dicc = gf.palabras_a_dicc(categorias)
    if eleccion == "1":
        delta_days = gf.delta_days_abs(lista_de_datos)
        gf.mostrar_lista_de_entradas(lista_de_datos[-60:])
        gpl.presentar_totales(
            categoria_dicc, lista_de_datos, delta_days,
            archivo_currency, valor_dolar
        )
    elif eleccion == "2":
        lista_de_datos, delta_days = gf.selector_de_periodo(lista_de_datos)
        gf.mostrar_lista_de_entradas(lista_de_datos)
        gpl.presentar_totales(
            categoria_dicc, lista_de_datos, delta_days,
            archivo_currency, valor_dolar
        )
    elif eleccion == "3":
        gpl.pie_gastos(categoria_dicc, lista_de_datos)
        delta_days = gf.delta_days_abs(lista_de_datos)
    elif eleccion == "4":
        gpl.ahorro_vs_tiempo(lista_de_datos)
        delta_days = gf.delta_days_abs(lista_de_datos)
