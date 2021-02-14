import re
from datetime import date
import funciones as gf


def transformar_fecha(d, m = 0, y = 0):
    return f"{['20'+y, y][len(y)!=2]}-{m.zfill(2)}-{d.zfill(2)}"


def recibir_movimiento():
    """This functions implements regex to flexibilize the input of date-amount-category.
    Then add the newString to the file and sorts the file by column."""
    # Regex pattern to use
    pattern_movimiento = re.compile(r'(?:(\d{1,2})[-\/](\d{1,2})[-\/](\d{2,4}))?\s?(-?\d+\.?\d*)\s([iIhHcCaAvVsS])?')
    movimiento = input("Ingresar movimiento (date amount C): ") + " " #Agrego el espacio para zafar con la regex FIX IT!
    # Apply the regex to the input and get a string
    movimientos = pattern_movimiento.findall(movimiento)
    fecha = date.today().isoformat()
    for items in movimientos:
        d, m, y, monto, categoria = items
        if not d == '':  # if not empty -> today or last used date
            fecha = transformar_fecha(d,m,y)
        if categoria == '':
            categoria = "V"
    return fecha, monto, categoria

def recibir_fecha(fecha_para_analizar):
    """Get a date with flexible format and return a date isoformat object"""
    pattern_fecha = re.compile(r'(\d{1,2})[-\/]?(\d{1,2})?[-\/]?(\d{2,4})?')
    fecha = pattern_fecha.findall(fecha_para_analizar)[0] # --> tuple
    fecha_list = [fecha[x] for x in range(len(fecha)) if fecha[x] != '']
    """TENGO QUE ACHICAR ESTO, FUSIONAR CON TRANSFORMAR_FECHA. SE VE MUY FEO Y NO SE ENTIENDE"""
    y_hoy, m_hoy, d_hoy = date.today().isoformat().split("-")
    if len(fecha_list) == 1:
        fecha_list.append(m_hoy)
        fecha_list.append(y_hoy)
    elif len(fecha_list) == 2:
        fecha_list.append(y_hoy)
    fecha = transformar_fecha(fecha_list[0], fecha_list[1], fecha_list[2])
    return date.fromisoformat(fecha)
