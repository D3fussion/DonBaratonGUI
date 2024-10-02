from pathlib import Path
from tkinter import Button, PhotoImage

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

import gui
import gui1
import gui2
import gui3
from get_db_connection import get_db_connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def obtener_datos(dato: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SET search_path TO "MercadoOnline";')
    if dato == 1:
        sql = """
            SELECT c.nombre_categoria, COUNT(o.id) AS productos_vendidos
            FROM ordenes o
            JOIN productos p ON o.producto = p.id
            JOIN categorias c ON p.categorias = c.id
            GROUP BY c.nombre_categoria;
            """
    elif dato == 2:
        sql = """
            SELECT p.nombre, SUM(o.cantidad) AS total_vendido
            FROM ordenes o
            JOIN productos p ON o.producto = p.id
            GROUP BY p.nombre
            ORDER BY total_vendido DESC
            LIMIT 10;
        """
    elif dato == 3:
        sql = """
            SELECT DATE(o.fecha_compra) AS fecha, SUM(o.cantidad) AS total_vendido
            FROM ordenes o
            GROUP BY fecha
            ORDER BY fecha;
        """
    else:
        sql = """
            SELECT o.email_usuario, COUNT(o.id) AS frecuencia_compras
            FROM ordenes o
            GROUP BY o.email_usuario
            ORDER BY frecuencia_compras DESC;

        """

    cur.execute(sql)
    resultados = cur.fetchall()

    # Cierra la conexión
    cur.close()
    conn.close()

    return resultados

def generar_fechas_con_rango(fecha_inicio, fecha_fin):
    # Genera una lista de fechas entre fecha_inicio y fecha_fin
    rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin).to_pydatetime().tolist()
    return rango_fechas

def mostrar_grafico_pastel(canvas_tk, option: bool):
    global chart
    if option:
        chart.get_tk_widget().destroy()
        matplotlib.pyplot.close()
    # Obtener los datos
    resultados = obtener_datos(1)

    # Separar los datos
    categorias = [fila[0] for fila in resultados]
    productos_vendidos = [fila[1] for fila in resultados]

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots()

    # Crear la gráfica de pastel
    ax.pie(productos_vendidos, labels=categorias, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegura que el gráfico sea circular
    ax.set_title('Sales By Product Category')

    # Incrustar la gráfica en el canvas de Tkinter
    chart = FigureCanvasTkAgg(fig, canvas_tk)
    chart.get_tk_widget().place(x=20, y=160, width=559, height=430)

# Los mensajes deben ser en ingles

def mostrar_grafico_barras(canvas_tk):
    global chart
    chart.get_tk_widget().destroy()
    matplotlib.pyplot.close()
    # Obtener los datos
    resultados = obtener_datos(2)

    # Separar los datos
    productos = [fila[0] for fila in resultados]
    total_vendido = [fila[1] for fila in resultados]

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots()

    # Crear la gráfica de barras
    ax.barh(productos, total_vendido, color='#47A6FF')
    ax.set_xlabel('Total Sold')
    ax.set_title('Best-Selling Products')

    # Incrustar la gráfica en el canvas de Tkinter
    chart = FigureCanvasTkAgg(fig, canvas_tk)
    chart.get_tk_widget().place(x=20, y=160, width=559, height=430)

def mostrar_grafico_lineas(canvas_tk):
    global chart
    chart.get_tk_widget().destroy()
    matplotlib.pyplot.close()
    # Obtener los datos de ventas por día
    resultados = obtener_datos(3)

    # Separar las fechas y las ventas
    fechas_existentes = [fila[0] for fila in resultados]
    ventas_existentes = [fila[1] for fila in resultados]

    # Rango de fechas
    fecha_inicio = fechas_existentes[0]
    fecha_fin = fechas_existentes[-1]

    # Generar todas las fechas entre la primera y la última
    todas_las_fechas = generar_fechas_con_rango(fecha_inicio, fecha_fin)

    # Crear un diccionario con todas las fechas (rellenadas con 0)
    ventas_por_dia = {fecha: 0 for fecha in todas_las_fechas}

    # Rellenar los días en los que hubo ventas
    for fecha, ventas in zip(fechas_existentes, ventas_existentes):
        ventas_por_dia[fecha] = ventas

    # Convertir el diccionario a listas para la gráfica
    fechas = list(ventas_por_dia.keys())
    ventas = list(ventas_por_dia.values())

    # Crear la figura de Matplotlib
    fig, ax = plt.subplots()

    # Crear la gráfica de líneas
    ax.plot(fechas, ventas, color='#47A6FF', marker='o', linestyle='-', linewidth=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Evolution Of Daily Sales')
    ax.tick_params(axis='x', rotation=45)

    # Incrustar la gráfica en el canvas de Tkinter
    chart = FigureCanvasTkAgg(fig, canvas_tk)
    chart.get_tk_widget().place(x=20, y=160, width=559, height=430)

def mostrar_grafico_dispersion(canvas_tk):
    global chart
    chart.get_tk_widget().destroy()
    matplotlib.pyplot.close()
    # Obtener los datos de frecuencia de compra por cliente
    resultados = obtener_datos(4)

    # Separar los emails y la frecuencia de compras
    emails = [fila[0] for fila in resultados]
    frecuencia_compras = [fila[1] for fila in resultados]

    # Generar índices para el eje x (solo para diferenciar a los clientes)
    indices_clientes = list(range(len(emails)))


    fig, ax = plt.subplots()

    ax.scatter(indices_clientes, frecuencia_compras, color='#47A6FF', s=100, alpha=0.6)
    ax.set_xlabel('Customer (Index)')
    ax.set_ylabel('Purchase Frequency')
    ax.set_title('Purchase Frequency Per Customer')

    # Incrustar la gráfica en el canvas de Tkinter
    chart = FigureCanvasTkAgg(fig, canvas_tk)
    chart.get_tk_widget().place(x=20, y=160, width=559, height=430)

def crear_gui(canvas, windows):
    global button_image_1, button_image_2, button_image_3, button_image_4, button_image_5, button_image_6, button_image_7, button_image_8, button_image_9
    global image_image_1, entry_image_1

    canvas.create_rectangle(
        0.0,
        5.684341886080802e-14,
        600.0,
        60.00000000000006,
        fill="#47A6FF",
        outline="")

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_gui(windows, "", canvas),
        relief="flat"
    )
    button_1.place(
        x=226.0,
        y=16.000000000000057,
        width=54.0,
        height=27.0
    )

    canvas.create_rectangle(
        0.0,
        60.00000000000006,
        600.0,
        69.00000000000006,
        fill="#478AC9",
        outline="")

    canvas.create_rectangle(
        0.0,
        598.0,
        600.0,
        624.0,
        fill="#478AC9",
        outline="")

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_gui(windows, "3", canvas),
        relief="flat"
    )
    button_2.place(
        x=426.0,
        y=16.000000000000057,
        width=53.0,
        height=27.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_gui(windows, "2", canvas),
        relief="flat"
    )
    button_3.place(
        x=354.0,
        y=16.000000000000057,
        width=55.0,
        height=27.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_gui(windows, "1", canvas),
        relief="flat"
    )
    button_4.place(
        x=297.0,
        y=16.000000000000057,
        width=40.0,
        height=27.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("No se abre ventana"),
        relief="flat"
    )
    button_5.place(
        x=496.0,
        y=16.000000000000057,
        width=74.0,
        height=27.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        82.0,
        29.000000000000057,
        image=image_image_1
    )

    canvas.create_text(
        269.0,
        88.00000000000006,
        anchor="nw",
        text="CHARTS",
        fill="#000000",
        font=("Roboto SemiBold", 16 * -1)
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button( # Sales by product category
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: mostrar_grafico_pastel(canvas, True),
        relief="flat"
    )
    button_6.place(
        x=22.0,
        y=126.00000000000006,
        width=138.0,
        height=36.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button( # Best-selling products
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: mostrar_grafico_barras(canvas),
        relief="flat"
    )
    button_7.place(
        x=182.0,
        y=126.00000000000006,
        width=107.0,
        height=36.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button( # Purchace frequency by user
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: mostrar_grafico_dispersion(canvas),
        relief="flat"
    )
    button_8.place(
        x=440.0,
        y=126.00000000000006,
        width=138.0,
        height=36.0
    )

    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button( # Evolution of sales
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: mostrar_grafico_lineas(canvas),
        relief="flat"
    )
    button_9.place(
        x=311.0,
        y=126.00000000000006,
        width=107.0,
        height=36.0
    )

    # canvas.create_rectangle(
    #     39.0,
    #     160.00000000000006,
    #     560.0,
    #     545.0,
    #     fill="#D9D9D9",
    #     outline=""
    # )

    mostrar_grafico_pastel(canvas, False)

def eliminar_gui(window, id: str, canvas):
    # Eliminar todos los widgets de la ventana
    for widget in window.winfo_children():
        if widget != canvas:
            widget.destroy()

    canvas.delete("all")
    chart.get_tk_widget().destroy()

    if id == "":
        gui.crear_gui(canvas, window)
    elif id == "1":
        gui1.crear_gui(canvas, window)
    elif id == "2":
        gui2.crear_gui(canvas, window)
    elif id == "3":
        gui3.crear_gui(canvas, window)
