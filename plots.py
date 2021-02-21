import matplotlib.pyplot as plt
import funciones as gf
import prompts as gp
import subprocess
import socket
import numpy as np
import datetime as date
import pandas as pd

dolar_subprocess = "/home/test/programitas/python_projects/guita/dolar_hoy"
REMOTE_SERVER = "one.one.one.one"
hoy = date.date.today()

def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


def valor_dolar_hoy(dolar_subprocess, REMOTE_SERVER):
    """
    La función detecta si hay conexión a inet. Si hay conexión,
    baja el valor del dolar de hoy, si no, usa el último valor
    encontrado la última vez que sí hubo conexión.
    """
    if is_connected(REMOTE_SERVER):
        valor_dolar = round(float(subprocess.check_output("curl -s rate.sx/1NZD", shell=True)) * 0.998,4)
        with open(dolar_subprocess, mode="w+") as f:
            f.write(f"{valor_dolar}")
    else:
        with open(dolar_subprocess, mode="r") as f:
            for line in f:
                valor_dolar = float(line)
    return valor_dolar

valor_dolar = valor_dolar_hoy(dolar_subprocess, REMOTE_SERVER)

def anios_meses_y_dias(delta_days):
    if delta_days < 30:
        return ""
    elif 365 > delta_days >= 30:
        meses = int(delta_days // 30)
        dias = int(delta_days % 30)
        return f"({meses} meses y {dias} días)"
    else:
        years = int(delta_days // 365)
        years_r = int(delta_days % 365)
        meses =  years_r // 30
        dias = years_r % 30
    return f"{years} años, {meses} meses y {dias} dias"

def to_dolar(nzd):
    return f"({round((float(nzd) * valor_dolar))}USD)"


def presentar_totales(diccionario, lista, delta_days):
    gp. separador(1)
    totales = gf.totales_de_categorias(diccionario, lista)
    gasto = sum([values for key, values in totales.items() if key != "I"])
    gasto_2 = sum([values for key, values in totales.items() if key not in ["S", "I"]])
    ingreso = totales["I"]
    balance = ingreso - gasto
    print(f"Total de días: {delta_days:.0f} ({anios_meses_y_dias(delta_days)}) (1NZD={valor_dolar}USD)")
    print(f"Balance: {balance:.2f} NZD  {to_dolar(balance)}")
    balance_diario = balance / delta_days
    print(f"Balance promedio por día: {balance_diario:.2f}")
    gp.separador(1)
    for key, value in diccionario.items():
        total_categoria = gf.totales_de_categorias(diccionario, lista)[key]
        print(f"{value.title()}: {total_categoria:.2f} NZD {to_dolar(total_categoria)}")
    gp.separador(1, "-")
    print(f"Total gastos: {gasto:.2f} -- Gasto diario: {gasto/delta_days:.2f}")
    gp.separador(2)


def pie_gastos(dicc, lista):
    """Generates de pie chart with percentages of the categories"""
    cat = [values.title() for values in dicc.values()][1:]  # omito first col que es el ingreso
    totales_cat = [values for values in gf.totales_de_categorias(dicc, lista).values()][1:]
    plt.pie(totales_cat, labels=cat,
            autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
    plt.title('Our expenses')
    plt.show()


def ahorro_vs_tiempo(lista):
    """Voy a crear una lista con los ahorros parciales por día. Para cada día
    sumo los ingresos y resto los gastos."""
    total_dias = int(gf.delta_days_abs(lista)) + 1 # Corrigo con ese 1 para usarlo para contar
    first_day_object = date.date.fromisoformat(lista[0][0])
    delta = date.timedelta(days=1)
    tomorrow = hoy + delta
    # Armo una lista únicamente con las fechas para usar en el eje x
    dates = [ date.date.isoformat(first_day_object + date.timedelta(days=i)) for i in range(0, total_dias) ]
    ahorro_parcial = []
    ahorro_del_dia = float(0)
    # Loopeo en las fechas y la lista, si es un ingreso sumo si es un gasto resto.
    for fecha in dates:
        for item_lista in lista:
            if fecha == item_lista[0]:
                if item_lista[2] != "I":
                    ahorro_del_dia -= float(item_lista[1])
                else:
                    ahorro_del_dia += float(item_lista[1])
        ahorro_parcial.append([fecha,ahorro_del_dia])

    # Uso los numpy arrays, porque hace más fácil el ploteo para pintar bajo la curva.
    dates_col = np.array([ item[0] for item in ahorro_parcial ])
    ahorro_col = np.array([ item[1] for item in ahorro_parcial ])
    maximo = np.amax(ahorro_col) # Busco máximo para normalizar
    maximo_abs = np.where(ahorro_col == maximo) # Indice de máximo
    ahorro_col = ahorro_col / maximo * 100 # Normalizo

    # Tuneo los ticks
    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(20)) # Aparecen 20 ticks
    plt.gcf().autofmt_xdate(rotation = 60) # Angulo para rotar los xticks
    # Grafico una linea comun para el ahorro diario
    plt.plot_date(dates_col, ahorro_col, linestyle='solid', linewidth='3', marker = 'None')
    plt.fill_between(dates_col, ahorro_col, where = (ahorro_col > 0), alpha = 0.3, interpolate = True) # Para la condición era necesario el array del numpy
    plt.fill_between(dates_col, ahorro_col, where = (ahorro_col < 0), alpha = 0.3, interpolate = True) # Para la condición era necesario el array del numpy
    # plt.text(dates_col[-1],ahorro_col[-1], f'({dates_col[-1]},{ahorro_col[-1]})')
    plt.grid()
    plt.ylabel('Ahorro %')
    plt.tight_layout()
    plt.show(block = False) # El False lo pongo para que cuando aparezca el gráfico pueda seguir usando el programa sin necesidad de cerrar el gráfico.
