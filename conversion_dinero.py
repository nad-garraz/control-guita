import subprocess
import socket
import os

from numpy.lib import function_base
import user_data as gud


remote_server = "one.one.one.one"


def set_dolar_file(archivo_currency):
    currency_specific_file = "ex" + "_" + f"{archivo_currency}"
    dolar_file = os.path.join(
        gud.get_directorio_cambios(), currency_specific_file
    )  # Crea archivo con info del dolar
    return dolar_file


def is_connected(hostname):
    """
    Me fijo si hay internet
    """
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


def get_valor_dolar_hoy(dolar_file, remote_server, archivo_currency):
    """
    Si hay conexión, baja el valor del dolar de hoy, si no, usa el último valor
    encontrado la última vez que sí hubo conexión.
    """
    if is_connected(remote_server):
        if (archivo_currency == "ARS"):
            command = f"curl -sf 'https://api.bluelytics.com.ar/v2/latest' | jq -r '.blue.value_sell'"  # Recurso para poder poner variable en comand
            valor_dolar = 1/float(subprocess.check_output(command, shell=True))
        else:
            command = f"forx -f {archivo_currency} usd"  # Recurso para poder poner variable en comando
            valor_dolar = round(float(subprocess.check_output(command, shell=True)), 4)

            with open(dolar_file, mode="w+") as f:
                f.write(f"{valor_dolar},{archivo_currency}")
    else:
        with open(dolar_file, mode="r") as f:
            for line in f:
                valor_dolar = float(line.split(",")[0])
    return valor_dolar


def get_valor_dolar(dolar_file, remote_server, archivo_currency):
    # if archivo_currency == "ARS":
    #     dolar_hoy = input("¿Cuánto está el dólar hoy? \n")
    #     valor_dolar = 1 / float(dolar_hoy)
    # else:
    valor_dolar = get_valor_dolar_hoy(dolar_file, remote_server, archivo_currency)
    # return round(valor_dolar, 6)
    return valor_dolar


def to_dolar(cantidad_dinero, valor_dolar):
    return f"{round((float(cantidad_dinero) * valor_dolar))}USD"


def to_dolar2(cantidad_dinero, valor_dolar):
    return f"{round((float(cantidad_dinero) * valor_dolar), 2)}"
