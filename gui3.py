from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar, messagebox
from tkinter.ttk import Treeview
import gui
import gui1
import gui2
import gui4
from get_db_connection import get_db_connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

diccionario_id = {"usuarios": [], "ordenes": []}
diccionarios_tablas = {"usuarios": "", "ordenes": ""}

def hacer_tabla(tabla: str, pos: list, svpos: list, shpos: list, window):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SET search_path TO "MercadoOnline";')
    cursor.execute(f"SELECT * FROM {tabla}")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    # Extraer los IDs y agregarlos al diccionario
    diccionario_id[tabla] = [row[0] for row in data]

    # Crear tabla utilizando Treeview
    table = Treeview(window, columns=column_names, show='headings')

    if diccionarios_tablas[tabla] == "":
        diccionarios_tablas[tabla] = table

    # Definir los encabezados de la tabla
    for col in column_names:
        table.heading(col, text=col)
        table.column(col, width=100, stretch=False)

    # Insertar los datos en la tabla
    for row in data:
        table.insert("", "end", values=row)

    # Crear scrollbar vertical
    vsb = Scrollbar(window, orient="vertical", command=table.yview)
    vsb.place(x=svpos[0], y=svpos[1], height=svpos[2])
    table.configure(yscrollcommand=vsb.set)

    # Crear scrollbar horizontal (opcional)
    hsb = Scrollbar(window, orient="horizontal", command=table.xview)
    hsb.place(x=shpos[0], y=shpos[1], width=shpos[2])
    table.configure(xscrollcommand=hsb.set)

    # Posicionar la tabla en la ventana
    table.place(x=pos[0], y=pos[1], width=pos[2], height=pos[3])

    # Ajustar tamaño de las columnas automáticamente
    for col in column_names:
        table.column(col, width=100)

    connection.close()

def eliminar_comprobar(id: str, tabla: str, window):
    print(diccionario_id[tabla], id)
    if id == "":
        messagebox.showerror("Error", "ID cannot be empty")
        return
    elif int(id) not in diccionario_id[tabla]:
        messagebox.showerror("Error", "ID not found")
        return
    try:
        id = int(id)
    except ValueError:
        messagebox.showerror("Error", "ID must be an number")
        return

    print("Se eliminará el registro con ID", id)
    eliminar(tabla, id, window)


def eliminar(tabla: str, id: int, window):
    connection = get_db_connection()  # Obtener conexión a la base de datos
    cursor = connection.cursor()
    cursor.execute('SET search_path TO "MercadoOnline";')

    # Ejecutar la consulta de eliminación
    cursor.execute(f"DELETE FROM {tabla} WHERE id = {id}")

    # Hacer commit de la transacción
    connection.commit()

    connection.close()

    messagebox.showinfo("Success", "Record deleted successfully")

    update_table(tabla, window)


def update_table(tabla: str, window):
    for item in diccionarios_tablas[tabla].get_children():
        diccionarios_tablas[tabla].delete(item)
    if tabla == "usuarios":
        hacer_tabla(tabla, [36, 110, 521, 148], [557, 110, 148], [36, 258, 521], window)
    else:
        hacer_tabla(tabla, [34, 363, 521, 148], [555, 363, 148], [34, 511, 521], window)



def crear_gui(canvas, window):
    global entry_1, entry_2
    global button_image_1, button_image_2, button_image_3, button_image_4, button_image_5, button_image_6, button_image_7
    global image_image_1, entry_image_1, entry_image_2

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
        command=lambda: eliminar_gui(window, "", canvas),
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
        command=lambda: print("No se abre ventana"),
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
        command=lambda: eliminar_gui(window, "2", canvas),
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
        command=lambda: eliminar_gui(window, "1", canvas),
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
        command=lambda: eliminar_gui(window, "4", canvas),
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
        234.5,
        303.50000000000006,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=46.0,
        y=291.00000000000006,
        width=377.0,
        height=23.0
    )

    canvas.create_text(
        243.0,
        80.00000000000006,
        anchor="nw",
        text="ORDERS TABLE",
        fill="#000000",
        font=("Roboto SemiBold", 16 * -1)
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_comprobar(entry_1.get(), "usuarios", window),
        relief="flat"
    )
    button_6.place(
        x=457.0,
        y=291.00000000000006,
        width=100.0,
        height=25.0
    )

    # canvas.create_rectangle(
    #     36.0,
    #     110.00000000000006,
    #     557.0,
    #     258.00000000000006,
    #     fill="#D9D9D9",
    #     outline="")

    hacer_tabla("usuarios", [36, 110, 521, 148], [557, 110, 148], [36, 258, 521], window)

    # canvas.create_text(
    #     51.0,
    #     269.00000000000006,
    #     anchor="nw",
    #     text="DELETE ID",
    #     fill="#000000",
    #     font=("Roboto Regular", 12 * -1)
    # )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        232.5,
        556.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=44.0,
        y=544.0,
        width=377.0,
        height=23.0
    )

    canvas.create_text(
        249.0,
        333.00000000000006,
        anchor="nw",
        text="USERS TABLE",
        fill="#000000",
        font=("Roboto SemiBold", 16 * -1)
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: eliminar_comprobar(entry_2.get(), "ordenes", window),
        relief="flat"
    )
    button_7.place(
        x=455.0,
        y=544.0,
        width=100.0,
        height=25.0
    )

    # canvas.create_rectangle(
    #     34.0,
    #     363.00000000000006,
    #     555.0,
    #     511.00000000000006,
    #     fill="#D9D9D9",
    #     outline="")

    hacer_tabla("ordenes", [34, 363, 521, 148], [555, 363, 148], [34, 511, 521], window)

    # canvas.create_text(
    #     49.0,
    #     522.0,
    #     anchor="nw",
    #     text="DELETE ID",
    #     fill="#000000",
    #     font=("Roboto Regular", 12 * -1)
    # )

def eliminar_gui(window, id, canvas):
    # Eliminar todos los widgets de la ventana
    for widget in window.winfo_children():
        if widget != canvas:
            widget.destroy()

    canvas.delete("all")

    if id == "":
        gui.crear_gui(canvas, window)
    elif id == "1":
        gui1.crear_gui(canvas, window)
    elif id == "2":
        gui2.crear_gui(canvas, window)
    elif id == "4":
        gui4.crear_gui(canvas, window)
