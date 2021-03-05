import plots as gpl
import funciones as gf
import input_manipulation as gim


categoria_dicc = {"I" : "ingreso",
                  "H" : "hospedaje",
                  "C" : "comida",
                  "A" : "auto",
                  "V" : "varios",
                  "S" : "salud"}

def separador(lineas=1, simbolo="="):
    """asteriscs for decoration"""
    linea_separadora = simbolo * 55
    for linea in range(lineas):
        print(f"{linea_separadora}")


def principal_menu():
    separador(2)
    menu_dict = {"1": "Ingresar movimiento",
                 "2": "Info monetaria",
                 "3": "Corregir datos manualmente",
                 "4": "Salir"}
    for key, value in menu_dict.items():
        print(f"{key} - {value}")
    separador()


def option_two_menu():
    """Presents the data after asking for the period or
    dates to analize"""
    separador(1)
    menu_dict = {"1": "Toda la lista",
            "2": "Intervalo especial",
            "3": "Pie gastos",
            "4": "Historial del ahorro"}
    for k, v in menu_dict.items():
        print(f"{k} - {v}")
    separador(1)


def prompt_data(eleccion, lista_de_datos):
    if eleccion == "1":
        delta_days = gf.delta_days_abs(lista_de_datos)
        gf.mostrar_lista_de_entradas(lista_de_datos[-50:])
        gpl.presentar_totales(categoria_dicc, lista_de_datos, delta_days)
    elif eleccion == "2":
        lista_de_datos, delta_days = gf.selector_de_periodo(lista_de_datos)
        gf.mostrar_lista_de_entradas(lista_de_datos)
        gpl.presentar_totales(categoria_dicc, lista_de_datos, delta_days)
    elif eleccion == "3":
        gpl.pie_gastos(categoria_dicc, lista_de_datos)
        delta_days = gf.delta_days_abs(lista_de_datos)
    elif eleccion == "4":
        gpl.ahorro_vs_tiempo(lista_de_datos)
        delta_days = gf.delta_days_abs(lista_de_datos)
