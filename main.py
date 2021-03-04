import input_manipulation as gim
import funciones as gf
import prompts as gp
import user_data as gud

# Archivo con la información
archivo_de_datos = gud.get_archivo_datos()


def main():
    # Hago un bkp antes de modificar nada
    gud.backup_datos(archivo_de_datos)
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
