import matplotlib.pyplot as plt
import funciones as gf
import prompts as gp
import conversion_dinero as gcd

# import user_data as gud
import input_manipulation as gim
import numpy as np
import datetime as date

hoy = date.date.today()


def presentar_totales(diccionario, lista, delta_days, archivo_currency, valor_dolar):
    gp.separador(1)
    totales = gf.totales_de_categorias(diccionario, lista)
    gasto = sum([values for key, values in totales.items() if key != "I"])
    gasto = round(gasto, 1)
    gasto_diario = round(gasto / delta_days, 1)
    ingreso = totales["I"]
    balance = ingreso - gasto
    print(f"Comenzó hace: {delta_days:.0f} {gim.anios_meses_y_dias(delta_days)}")
    if archivo_currency == "USD":
        print(f"Balance: {balance:.2f}{archivo_currency}")
        balance_diario = round(balance / delta_days, 1)
        print(f"Balance promedio por día: {balance_diario:.2f} {archivo_currency}")
        gp.separador(1)
        for key, value in diccionario.items():
            total_categoria = round(
                gf.totales_de_categorias(diccionario, lista)[key], 1
            )
            print(f"{value.title()}: {total_categoria:,} {archivo_currency}")
        gp.separador(1, "-")
        print(f"Total gastos: {gasto:.0f} USD -- Gasto diario: {gasto_diario:,} USD")
    else:
        print(
            f"Balance: {balance:.2f} {archivo_currency} ({gcd.to_dolar(balance, valor_dolar)}) (1{archivo_currency}={valor_dolar}USD)"
        )
        balance_diario = balance / delta_days
        print(f"Balance promedio por día: {balance_diario:.0f}{archivo_currency}")
        gp.separador(1)
        for key, value in diccionario.items():
            total_categoria = round(
                gf.totales_de_categorias(diccionario, lista)[key], 1
            )
            if total_categoria == 0:  # Si el ingreso es 0, no aparece la categoría
                continue
            else:
                print(
                    f"{value.title():<10}:  {total_categoria:,}"
                    + f"{archivo_currency:<3} ({gcd.to_dolar(total_categoria, valor_dolar):>4})"
                )

        gp.separador(1, "-")
        print(
            f"Total gastos: {gasto:,} {archivo_currency} ({gcd.to_dolar(gasto, valor_dolar)}) -- Gasto diario: {gasto_diario:,} {archivo_currency}"
        )
    gp.separador(2)


def pie_gastos(dicc, lista):
    """
    Generates de pie chart with percentages of the categories
    TODO: Sacar categorías con 0%, también poner opción de sacar el ingreso.
    """
    totales_cat = []
    cat = []
    # totales_cat = [
    #         values for values in gf.totales_de_categorias(dicc, lista).values()
    #         ]
    # cat = [
    #     values.title() for values in dicc.values() if values.title()
    # ]  # Generates list with the names of the categories.

    print(gf.totales_de_categorias(dicc, lista))
    print(dicc)

    for item in gf.totales_de_categorias(dicc, lista).items():
        if (item[0] != 'I' and item[1] != 0): #  Saco al ingreso y a las categorías con valor nulo
            cat.append(dicc[item[0]])
            totales_cat.append(item[1])

    plt.pie(
        totales_cat, labels=cat, autopct="%1.1f%%", wedgeprops={"edgecolor": "black"}
    )
    plt.title("Our expenses")
    plt.show(block=False)


def ahorro_vs_tiempo(lista):
    """
    Voy a crear una lista con los ahorros parciales por día. Para cada día
    sumo los ingresos y resto los gastos.
    """
    total_dias = (
        int(gf.delta_days_abs(lista)) + 1
    )  # Corrigo con ese 1 para usarlo para contar
    first_day_object = date.date.fromisoformat(lista[0][0])
    # delta = date.timedelta(days = 1)
    # tomorrow = hoy + delta
    # Armo una lista únicamente con las fechas para usar en el eje x
    dates = [
        date.date.isoformat(first_day_object + date.timedelta(days=i))
        for i in range(0, total_dias)
    ]
    ahorro_parcial = []
    ahorro_del_dia = float(0)
    # Loopeo en las fechas y la lista, si es un ingreso sumo si es un gasto resto.
    for fecha in dates:
        for item_lista in lista:
            if fecha == item_lista[0]:
                if item_lista[3] != "I":
                    ahorro_del_dia -= float(item_lista[1])
                else:
                    ahorro_del_dia += float(item_lista[1])
        ahorro_parcial.append([fecha, ahorro_del_dia])

    # Uso los numpy arrays, porque hace más fácil el ploteo para pintar bajo la curva.
    dates_col = np.array([item[0] for item in ahorro_parcial])
    ahorro_col = np.array([item[1] for item in ahorro_parcial])
    # Busco el número para normalizar
    maximo = max([abs(item[1]) for item in ahorro_parcial])
    # maximo = np.amax(ahorro_col) # Busco máximo para normalizar
    # maximo_abs = np.where(ahorro_col == maximo) # Indice de máximo
    # ahorro_col = ahorro_col # Ahorro total
    ahorro_col = ahorro_col / maximo  # Normalizo

    # Tuneo los ticks
    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))  # Aparecen 20 ticks
    plt.gcf().autofmt_xdate(rotation=60)  # Angulo para rotar los xticks
    # Grafico una linea comun para el ahorro diario
    plt.plot_date(dates_col, ahorro_col, markersize=0, linestyle="solid", linewidth="3")
    plt.fill_between(
        dates_col, ahorro_col, where=(ahorro_col > 0), alpha=0.3, interpolate=True
    )  # Para la condición era necesario el array del numpy
    plt.fill_between(
        dates_col, ahorro_col, where=(ahorro_col < 0), alpha=0.3, interpolate=True
    )  # Para la condición era necesario el array del numpy
    plt.grid()
    plt.ylabel("Ahorro")
    plt.tight_layout()
    plt.show(
        block=False
    )  # El False lo pongo para que cuando aparezca el gráfico pueda seguir usando el programa sin necesidad de cerrar el gráfico.
