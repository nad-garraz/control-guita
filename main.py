import input_manipulation as gim
import funciones as gf
import prompts as gp
import user_data as gud
import conversion_dinero as gcd
import readline


def main():
    salir = False
    nuevo_ingreso = True
    nuevo_archivo = True
    while not salir:
        # Bloque que se encarga de juntar la informacion del archivo de datos
        # pasa cuando se pone un nuevo archivo o cuando se agrega una entrada a
        # los datos
        if nuevo_ingreso is not False:
            # Get archivo con la info que quiero trabajar
            archivo_de_datos = gud.get_current_archivo_datos()
            # Saco información en formato útil del archivo de datos
            lista_de_datos, archivo_currency, categorias = gf.archivo_a_lista(
                archivo_de_datos
            )
            nuevo_ingreso = False

        # Bloque que se encarga de la información cuando se pone
        # un nuevo archivo de datos
        if nuevo_archivo is not False:
            # Hago un bkp antes de modificar nada
            gud.backup_datos(archivo_de_datos)
            # Averiguo valor cambio a dólar.
            dolar_file = gcd.set_dolar_file(archivo_currency)
            valor_dolar = gcd.get_valor_dolar(
                dolar_file, gcd.remote_server, archivo_currency
            )
            # Muestra información sobre el archivo de datos en uso
            gp.intro_current_datos(archivo_de_datos, archivo_currency, categorias)
            nuevo_archivo = False

        # Prompt to choose
        gp.principal_menu()
        # Choice
        eleccion = gf.eleccion_usuario()
        if eleccion == "1":
            # Enter move
            gim.recibir_movimiento(archivo_de_datos, valor_dolar)
            gf.order_first_column_by_dates(archivo_de_datos)
            nuevo_ingreso = True
            # Ordeno el archivo
        elif eleccion == "2":
            gp.option_two_menu()
            eleccion = gf.eleccion_usuario()
            gp.prompt_data(
                eleccion, lista_de_datos, archivo_currency, categorias, valor_dolar
            )
        elif eleccion == "3":
            gf.editar_manual(archivo_de_datos)
            # Ordeno el archivo
            gf.order_first_column_by_dates(archivo_de_datos)
        elif eleccion == "4":
            gud.cambiar_archivo_datos()
            nuevo_archivo = True
            nuevo_ingreso = True
        # Quit loop
        elif eleccion in gf.exit:
            salir = True
            break


main()
