from datetime import date
import input_manipulation as gim
import plots as gpl
import os
exit = ["quit", "exit", "q", "4"]


def archivo_a_lista(archivo):
    """takes csv file and outputs a 3 column list"""
    with open(archivo, mode='r') as extracted_file:
        return [row.rstrip().split(",") for row in extracted_file]


def separador(lineas=1, symbol="="):
    """asteriscs for decoration"""
    linea_separadora = symbol*35
    for linea in range(lineas):
        print(f"{linea_separadora}")


def principal_menu():
    separador(2)
    menu_dict = {"1": "Ingresar movimiento",
                 "2": "Info monetaria",
                 "3": "Salir"}
    for key, value in menu_dict.items():
        print(f"{key} - {value}")
    separador()


def eleccion_usuario():
    """ TODO -> maybe try, except block??"""
    opcion_valida = {"1", "2","3","4"}.union(set(exit))
    while True:
        eleccion = str(input("Qué querés hacer?: "))
        if eleccion in opcion_valida:
            break
        else:
            print("¡Opción incorrecta! Ingresa una opción válida:")
    separador(2)
    return eleccion


def agregar_dato_a_archivo(fecha, monto, categoria, archivo):
    """writes a line of formated and coma separated values to file"""
    with open(archivo, mode="a+") as datos_file:
        datos_file.write(f"{fecha},{monto},{categoria}\n")

def mostrar_lista_de_entradas(lista):
    fecha_actual = lista[0][0][6]
    for indice, linea in enumerate(lista,1):
        fecha, monto, categoria = linea
        if fecha[6] != fecha_actual:
            fecha_actual = fecha[6]
            separador(symbol="-")
        print(f"{fecha}\t{monto}\t{categoria}\t{indice}\t{gpl.to_dolar(monto)}")

def delta_days_abs(lista):
    """ returns the days that passed between today and the first date of the csv file.
    The file has to be alphabeticaly sorted"""
    fecha_objeto1 = date.fromisoformat(lista[0][0])
    today = date.today()
    delta_days = str(today - fecha_objeto1).split(" ")[0]
    return float(delta_days)


def totales_de_categorias(diccionario, lista):
    """Returns a diccionary with the sum of all the elements of the categories I, H, C, A, V, S
    respectely.
    TODO: 'comprehension lists', super compact but hard to read... erase or not?"""
    dicc_categoria_totales = {}
    for categoria in diccionario.keys():
        lista_para_una_categoria = []
        for row in lista:
            if row[2][0] == categoria:
                lista_para_una_categoria.append(float(row[1]))
        total_de_categoria = round(sum(lista_para_una_categoria), 2)
        dicc_categoria_totales[categoria] = total_de_categoria
    return dicc_categoria_totales
    # return {categoria : round(sum([float(row[1]) for row in lista if row[2][0] == categoria]), 2) for categoria in diccionario.keys()}


def selector_de_periodo(lista):
    """TODO: Elegir periodo de fechas para analizar"""
    # Tomar una fecha inicial
    desde_fecha = input("Fecha inicial: ")
    desde_fecha = gim.recibir_fecha(desde_fecha)
    # Tomar una fecha final
    hasta_fecha = input("Fecha final (hoy): ")
    if hasta_fecha == '':
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
    os.system(f'$EDITOR {archivo}')

def order_first_column_by_dates(archivo):
    """FROM A LIST OF CSV, BEING DATES ON THE FIRST COLUMN,
    THE FUNCTION SORTS THE LINE BY DATES IN INCREASING ORDER"""
    with open(archivo, mode="r") as datos_file:
        lista = list(datos_file)
    for i in range(0, len(lista)):
        minimo_fecha = lista[i].split(",")[0]
        minimo_fecha_objeto = date.fromisoformat(minimo_fecha)
        for j in range(i+1, len(lista)):
            comparar_fecha = lista[j].split(",")[0]
            comparar_fecha_objeto = date.fromisoformat(comparar_fecha)
            if comparar_fecha_objeto < minimo_fecha_objeto:
                nuevo_minimo_lista = lista[j]
                minimo_fecha = lista[j].split(",")[0]
                minimo_fecha_objeto = date.fromisoformat(minimo_fecha)
                lista[j] = lista[i]
                lista[i] = nuevo_minimo_lista
    with open(archivo, mode="w") as do:
        for linea in lista:
            do.write(linea)
