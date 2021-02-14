from datetime import *

archivo="datos.csv"

def order_list_by_dates(archivo):
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
    return lista

lista = order_list_by_dates(archivo)

with open("datos_ordenados.csv", mode="w") as do:
    for linea in lista:
        do.write(linea)
