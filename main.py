import input_manipulation as gim
import funciones as gf
import prompts as gp


# Archivo con la información
archivo_de_datos = "/home/test/programitas/python_projects/guita/datos.csv"
# Archivo copiado bkp antes de editar nada
archivo_de_datos_bkp = "/home/test/programitas/python_projects/guita/datos.tar.bzip2"


def main():
    # Hago un bkp antes de modificar nada
    gf.do_backup(archivo_de_datos, archivo_de_datos_bkp)
    while True:
        # Make the list of data that its easier to work with
        lista_de_datos = gf.archivo_a_lista(archivo_de_datos)
        # Prompt to choose
        gp.principal_menu()
        # Choice
        eleccion = gf.eleccion_usuario()
        if eleccion == "1":
            # Enter move
            gim.recibir_movimiento(archivo_de_datos)
            # Ordeno el archivo
            gf.order_first_column_by_dates(archivo_de_datos)
        elif eleccion == "2":
            gp.option_two_menu()
            eleccion = gf.eleccion_usuario()
            gp.prompt_data(eleccion, lista_de_datos)
        elif eleccion == "3":
            gf.editar_manual(archivo_de_datos)
            # Ordeno el archivo
            gf.order_first_column_by_dates(archivo_de_datos)
        # Quit loop
        elif eleccion in gf.exit:
            break


main()
