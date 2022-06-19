import re
from datetime import date
import funciones as gf
import curses


def transformar_fecha(d, m=0, y=0):
    return f"{['20'+y, y][len(y)!=2]}-{m.zfill(2)}-{d.zfill(2)}"


def recibir_movimiento(archivo, valor_dolar):
    """
    This functions implements regex to flexibilize
    the input of date-amount-category.
    Then add the newString to the file and sorts the file by column.
    """
    # Regex pattern to use
    pattern_movimiento = re.compile(
        r"(?:(\d{1,2})[-\/](\d{1,2})[-\/](\d{2,4}))?\s?(-?\d+\.?\d*)\s([a-zA-Z])?"
    )
    movimiento = (
        input("Ingresar movimiento (date amount C): ") + " "
    )  # Agrego el espacio para zafar con la regex FIX IT!
    # Apply the regex to the input and get a string
    movimientos = pattern_movimiento.findall(movimiento)
    fecha = date.today().isoformat()
    # lista_movimientos = []
    for items in movimientos:
        d, m, y, monto, categoria = items
        if not d == "":  # if not empty -> today or last used date
            fecha = transformar_fecha(d, m, y)
        if categoria == "":
            categoria = "V"
        else:
            categoria = categoria.capitalize()  # scula porque queda lindo
        print(f"{fecha} {monto} {categoria}")
        gf.agregar_dato_a_archivo(fecha, monto, categoria, archivo, valor_dolar)


def recibir_fecha(fecha_para_analizar):
    """
    Get a date with flexible format and return a date isoformat object
    """
    pattern_fecha = re.compile(r"(\d{1,2})[-\/]?(\d{1,2})?[-\/]?(\d{2,4})?")
    fecha = pattern_fecha.findall(fecha_para_analizar)[0]  # --> tuple
    fecha_list = [fecha[x] for x in range(len(fecha)) if fecha[x] != ""]
    """
    TENGO QUE ACHICAR ESTO, FUSIONAR CON TRANSFORMAR_FECHA.
    SE VE MUY FEO Y NO SE ENTIENDE
    """
    y_hoy, m_hoy, d_hoy = date.today().isoformat().split("-")
    if len(fecha_list) == 1:
        fecha_list.append(m_hoy)
        fecha_list.append(y_hoy)
    elif len(fecha_list) == 2:
        fecha_list.append(y_hoy)
    fecha = transformar_fecha(fecha_list[0], fecha_list[1], fecha_list[2])
    return date.fromisoformat(fecha)


def anios_meses_y_dias(delta_days):
    if delta_days < 30:
        return "días"
    elif 30 <= delta_days < 365:
        meses = int(delta_days // 30)
        dias = int(delta_days % 30)
        return f"({meses} meses y {dias} días)"
    else:
        years = int(delta_days // 365)
        years_r = int(delta_days % 365)
        meses = years_r // 30
        dias = years_r % 30
    return f"({years} años, {meses} meses y {dias} dias)"
