import os
import webbrowser
from pathlib import Path
from tkinter import Entry, Button, PhotoImage, Scrollbar, messagebox, Tk, Canvas
from tkinter.ttk import Treeview
from psycopg2.extras import RealDictCursor
from get_db_connection import get_db_connection
import gui
import gui2
import gui3
import gui4

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def hacer_tabla(tabla: str, windows):
    global table
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Crear tabla utilizando Treeview
    table = Treeview(windows, columns=column_names, show='headings')

    # Definir los encabezados de la tabla
    for col in column_names:
        table.heading(col, text=col)
        table.column(col, width=100, stretch=False)

    # Insertar los datos en la tabla
    for row in data:
        table.insert("", "end", values=row)

    # Crear scrollbar vertical
    vsb = Scrollbar(windows, orient="vertical", command=table.yview)
    vsb.place(x=560, y=196, height=235)
    table.configure(yscrollcommand=vsb.set)

    # Crear scrollbar horizontal (opcional)
    hsb = Scrollbar(windows, orient="horizontal", command=table.xview)
    hsb.place(x=39, y=431, width=521)
    table.configure(xscrollcommand=hsb.set)

    # Posicionar la tabla en la ventana
    table.place(x=39, y=196, width=521, height=235)

    # Ajustar tamaño de las columnas automáticamente
    for col in column_names:
        table.column(col, width=100)

    connection.close()


def actualizar_tabla(tabla: str, windows):
    for item in table.get_children():
        table.delete(item)
    hacer_tabla(tabla, windows)


def conseguir_datos(id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
       SELECT p.*, c.nombre_categoria 
       FROM productos p 
       LEFT JOIN categorias c ON p.categorias = c.id 
       WHERE p.id = %s
    """, (int(id),))
    product = cursor.fetchone()
    conn.close()
    if product:
        return dict(product)
    else:
        return {"error": "Product not found"}


def see_page(id: str):
    if not id:
        messagebox.showerror("Error", "No product selected")
        return
    elif not id.isdigit():
        messagebox.showerror("Error", "Invalid product ID")
        return

    datos = conseguir_datos(id)
    print(datos)

    if "error" in datos:
        messagebox.showerror("Error", datos["error"])
        return

    with open("assets/pagina/artic.js", "r") as f:
        lineas = f.readlines()

    datos["precio_antes_descuento"] = str(datos["precio_antes_descuento"])
    datos["precio_despues_descuento"] = str(datos["precio_despues_descuento"])

    lineas[0] = f"var productoSeleccionado = {datos};\n"

    with open("assets/pagina/artic.js", "w") as f:
        f.writelines(lineas)

    link_completo = os.path.abspath("assets/pagina/artic.html")
    webbrowser.open(link_completo)

def crear_gui(canvas, windows):
    global button_image_1, button_image_2, button_image_3, button_image_4, button_image_5
    global button_image_6, button_image_7, button_image_8, button_image_9, button_image_10
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
        command=lambda: print("No abre ventana"),
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
        command=lambda: eliminar_gui(windows, "4", canvas),
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

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        237.5,
        537.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=49.0,
        y=525.0,
        width=377.0,
        height=23.0
    )

    canvas.create_text(
        254.0,
        90.00000000000006,
        anchor="nw",
        text="SQL TABLES",
        fill="#000000",
        font=("Roboto SemiBold", 16 * -1)
    )

    canvas.create_text(
        233.0,
        469.00000000000006,
        anchor="nw",
        text="PRODUCT VIEWER",
        fill="#000000",
        font=("Roboto SemiBold", 16 * -1)
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: actualizar_tabla("productos", windows),
        relief="flat"
    )
    button_6.place(
        x=39.0,
        y=134.00000000000006,
        width=100.0,
        height=25.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: actualizar_tabla("usuarios", windows),
        relief="flat"
    )
    button_7.place(
        x=180.0,
        y=134.00000000000006,
        width=100.0,
        height=25.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: actualizar_tabla("categorias", windows),
        relief="flat"
    )
    button_8.place(
        x=460.0,
        y=134.00000000000006,
        width=100.0,
        height=25.0
    )

    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: see_page(entry_1.get()),
        relief="flat"
    )
    button_9.place(
        x=460.0,
        y=525.0,
        width=100.0,
        height=25.0
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: actualizar_tabla("ordenes", windows),
        relief="flat"
    )
    button_10.place(
        x=320.0,
        y=134.00000000000006,
        width=100.0,
        height=25.0
    )

    hacer_tabla("usuarios", windows)

    canvas.create_text(
        55.0,
        503.00000000000006,
        anchor="nw",
        text="INSERT ID",
        fill="#000000",
        font=("Roboto Regular", 12 * -1)
    )

def eliminar_gui(window, id: str, canvas):
    # Eliminar todos los widgets de la ventana
    for widget in window.winfo_children():
        if widget != canvas:
            widget.destroy()

    canvas.delete("all")

    if id == "":
        gui.crear_gui(canvas, window)
    elif id == "2":
        gui2.crear_gui(canvas, window)
    elif id == "3":
        gui3.crear_gui(canvas, window)
    elif id == "4":
        gui4.crear_gui(canvas, window)