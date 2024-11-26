import os
import webbrowser
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, END
from psycopg2.extras import RealDictCursor
from get_db_connection import get_db_connection
import gui
import gui1
import gui3
import gui4

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def conseguir_datos_internos():
    name = entry_1.get()
    overview = entry_2.get("1.0", "end-1c")
    description = entry_3.get("1.0", "end-1c")
    additional_info = entry_4.get("1.0", "end-1c")
    category = entry_5.get()
    price_before = entry_6.get()
    price_after = entry_7.get()
    stock = entry_8.get()
    image_1 = entry_9.get()
    image_2 = entry_10.get()
    image_3 = entry_11.get()

    try:
        price_before = float(price_before)
        price_after = float(price_after)
        stock = int(stock)
    except ValueError:
        return {"error": "Price, stock and category must be numbers"}

    if name == "" or overview == "" or description == "" or additional_info == "" or category == "" or price_before == "" or price_after == "" or stock == "" or image_1 == "" or image_2 == "" or image_3 == "":
        return {"error": "All fields must be filled"}
    elif not category.isnumeric():
        return {"error": "Price, stock and category must be numbers"}
    elif not image_1.startswith("http") or not image_2.startswith("http") or not image_3.startswith("http"):
        return {"error": "Image links must start with 'http'"}
    else:
        return {
            "nombre": name,
            "overview": overview,
            "descripcion": description,
            "datos_adicionales": additional_info,
            "categorias": category,
            "precio_antes_descuento": (round(float(price_before) * 100)) / 100,
            "precio_despues_descuento": (round(float(price_after) * 100)) / 100,
            "stock_disponible": stock,
            "link_imagen1": image_1,
            "link_imagen2": image_2,
            "link_imagen3": image_3
        }

def conseguir_datos(id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
       SELECT * FROM productos WHERE id = %s
    """, (int(id),))
    product = cursor.fetchone()
    conn.close()
    if product:
        return dict(product)
    else:
        return {"error": "Product not found"}


def buscar_datos(id: str):
    if not id:
        messagebox.showerror("Error", "No product selected")
        return
    elif not id.isdigit():
        messagebox.showerror("Error", "Invalid product ID")
        return

    product = conseguir_datos(id)

    if "error" in product:
        messagebox.showerror("Error", "Product not found")
        return

    limpiar(False)

    entry_1.insert(0, product["nombre"])
    entry_2.insert("1.0", product["overview"])
    entry_3.insert("1.0", product["descripcion"])
    entry_4.insert("1.0", product["datos_adicionales"])
    entry_5.insert(0, product["categorias"])
    entry_6.insert(0, product["precio_antes_descuento"])
    entry_7.insert(0, product["precio_despues_descuento"])
    entry_8.insert(0, product["stock_disponible"])
    entry_9.insert(0, product["link_imagen1"])
    entry_10.insert(0, product["link_imagen2"])
    entry_11.insert(0, product["link_imagen3"])

def see_page():
    datos = conseguir_datos_internos()
    print(datos)
    if "error" in datos:
        messagebox.showerror("Error", datos["error"])
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_categoria FROM categorias WHERE id = %s", (datos["categorias"],))
    categoria = cursor.fetchone()[0]
    conn.close()
    datos["nombre_categoria"] = categoria
    datos["precio_antes_descuento"] = "{:.2f}".format(datos["precio_antes_descuento"])
    datos["precio_despues_descuento"] = "{:.2f}".format(datos["precio_despues_descuento"])

    with open("assets/pagina/artic.js", "r") as f:
        lineas = f.readlines()

    lineas[0] = f"var productoSeleccionado = {datos};\n"

    with open("assets/pagina/artic.js", "w") as f:
        f.writelines(lineas)

    link_completo = os.path.abspath("assets/pagina/artic.html")
    webbrowser.open(link_completo)

def actualizar_datos():
    datos = conseguir_datos_internos()
    if "error" in datos:
        messagebox.showerror("Error", datos["error"])
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos 
        SET nombre = %s, overview = %s, descripcion = %s, datos_adicionales = %s, categorias = %s, precio_antes_descuento = %s, precio_despues_descuento = %s, stock_disponible = %s, link_imagen1 = %s, link_imagen2 = %s, link_imagen3 = %s
        WHERE id = %s
    """, (datos["nombre"], datos["overview"], datos["descripcion"], datos["datos_adicionales"], datos["categorias"], datos["precio_antes_descuento"], datos["precio_despues_descuento"], datos["stock_disponible"], datos["link_imagen1"], datos["link_imagen2"], datos["link_imagen3"], entry_12.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Product updated successfully")
    limpiar(True)

def limpiar(desabilitar: bool):
    entry_12.delete(0, END)
    entry_1.delete(0, END)
    entry_2.delete("1.0", END)
    entry_3.delete("1.0", END)
    entry_4.delete("1.0", END)
    entry_5.delete(0, END)
    entry_6.delete(0, END)
    entry_7.delete(0, END)
    entry_8.delete(0, END)
    entry_9.delete(0, END)
    entry_10.delete(0, END)
    entry_11.delete(0, END)

    if desabilitar:
        entry_1.config(state="disabled")
        entry_2.config(state="disabled")
        entry_2.config(bg="#F0F0F0")
        entry_3.config(state="disabled")
        entry_3.config(bg="#F0F0F0")
        entry_4.config(state="disabled")
        entry_4.config(bg="#F0F0F0")
        entry_5.config(state="disabled")
        entry_6.config(state="disabled")
        entry_7.config(state="disabled")
        entry_8.config(state="disabled")
        entry_9.config(state="disabled")
        entry_10.config(state="disabled")
        entry_11.config(state="disabled")
    else:
        entry_1.config(state="normal")
        entry_2.config(state="normal")
        entry_2.config(bg="#E9F2FA")
        entry_3.config(state="normal")
        entry_3.config(bg="#E9F2FA")
        entry_4.config(state="normal")
        entry_4.config(bg="#E9F2FA")
        entry_5.config(state="normal")
        entry_6.config(state="normal")
        entry_7.config(state="normal")
        entry_8.config(state="normal")
        entry_9.config(state="normal")
        entry_10.config(state="normal")
        entry_11.config(state="normal")

def crear_gui(canvas, window):
    global button_image_1, button_image_2, button_image_3, button_image_4, button_image_5
    global button_image_6, button_image_7, button_image_8, button_image_9, button_image_10
    global image_image_1, entry_image_1, entry_image_2, entry_image_3, entry_image_4, entry_image_5
    global entry_image_6, entry_image_7, entry_image_8, entry_image_9, entry_image_10, entry_image_11, entry_image_12
    global entry_1, entry_2, entry_3, entry_4, entry_5, entry_6, entry_7, entry_8, entry_9, entry_10, entry_11, entry_12

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
        command=lambda: eliminar_gui(window, "3", canvas),
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
        command=lambda: print("No se abre ventana"),
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
        242.5,
        170.50000000000006,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_1.place(
        x=34.0,
        y=158.00000000000006,
        width=417.0,
        height=23.0
    )

    canvas.create_text(
        35.0,
        137.00000000000006,
        anchor="nw",
        text="NAME",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        300.0,
        236.00000000000006,
        image=entry_image_2
    )
    entry_2 = Text(
        bd=0,
        bg="#F0F0F0",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_2.place(
        x=34.0,
        y=211.00000000000006,
        width=532.0,
        height=48.0
    )

    canvas.create_text(
        35.0,
        190.00000000000006,
        anchor="nw",
        text="OVERVIEW",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        300.0,
        318.00000000000006,
        image=entry_image_3
    )
    entry_3 = Text(
        bd=0,
        bg="#F0F0F0",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_3.place(
        x=34.0,
        y=293.00000000000006,
        width=532.0,
        height=48.0
    )

    canvas.create_text(
        35.0,
        272.00000000000006,
        anchor="nw",
        text="DESCRIPTION",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        300.0,
        396.00000000000006,
        image=entry_image_4
    )
    entry_4 = Text(
        bd=0,
        bg="#F0F0F0",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_4.place(
        x=34.0,
        y=371.00000000000006,
        width=532.0,
        height=48.0
    )

    canvas.create_text(
        35.0,
        350.00000000000006,
        anchor="nw",
        text="ADDITIONAL INFO",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        529.0,
        170.50000000000006,
        image=entry_image_5
    )
    entry_5 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_5.place(
        x=492.0,
        y=158.00000000000006,
        width=74.0,
        height=23.0
    )

    canvas.create_text(
        482.0,
        137.00000000000006,
        anchor="nw",
        text="CATEGORY",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        109.0,
        461.50000000000006,
        image=entry_image_6
    )
    entry_6 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_6.place(
        x=34.0,
        y=449.00000000000006,
        width=150.0,
        height=23.0
    )

    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        300.0,
        461.50000000000006,
        image=entry_image_7
    )
    entry_7 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_7.place(
        x=225.0,
        y=449.00000000000006,
        width=150.0,
        height=23.0
    )

    entry_image_8 = PhotoImage(
        file=relative_to_assets("entry_8.png"))
    entry_bg_8 = canvas.create_image(
        491.0,
        461.50000000000006,
        image=entry_image_8
    )
    entry_8 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_8.place(
        x=416.0,
        y=449.00000000000006,
        width=150.0,
        height=23.0
    )

    canvas.create_text(
        35.0,
        428.00000000000006,
        anchor="nw",
        text="PRICE (BEFORE)",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    canvas.create_text(
        226.0,
        428.00000000000006,
        anchor="nw",
        text="PRICE (AFTER)",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    canvas.create_text(
        417.0,
        428.00000000000006,
        anchor="nw",
        text="STOCK",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    entry_image_9 = PhotoImage(
        file=relative_to_assets("entry_9.png"))
    entry_bg_9 = canvas.create_image(
        109.0,
        514.5,
        image=entry_image_9
    )
    entry_9 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_9.place(
        x=34.0,
        y=502.00000000000006,
        width=150.0,
        height=23.0
    )

    entry_image_10 = PhotoImage(
        file=relative_to_assets("entry_10.png"))
    entry_bg_10 = canvas.create_image(
        300.0,
        514.5,
        image=entry_image_10
    )
    entry_10 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_10.place(
        x=225.0,
        y=502.00000000000006,
        width=150.0,
        height=23.0
    )

    entry_image_11 = PhotoImage(
        file=relative_to_assets("entry_11.png"))
    entry_bg_11 = canvas.create_image(
        491.0,
        514.5,
        image=entry_image_11
    )
    entry_11 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0,
        state="disabled"
    )
    entry_11.place(
        x=416.0,
        y=502.00000000000006,
        width=150.0,
        height=23.0
    )

    canvas.create_text(
        35.0,
        481.00000000000006,
        anchor="nw",
        text="IMAGE 1",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    canvas.create_text(
        226.0,
        481.00000000000006,
        anchor="nw",
        text="IMAGE 2",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    canvas.create_text(
        417.0,
        481.00000000000006,
        anchor="nw",
        text="IMAGE 3",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: see_page(),
        relief="flat"
    )
    button_6.place(
        x=124.0,
        y=544.0,
        width=159.0,
        height=37.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: actualizar_datos(),
        relief="flat"
    )
    button_7.place(
        x=315.0,
        y=544.0,
        width=159.0,
        height=37.0
    )

    entry_image_12 = PhotoImage(
        file=relative_to_assets("entry_12.png"))
    entry_bg_12 = canvas.create_image(
        235.0,
        108.50000000000006,
        image=entry_image_12
    )
    entry_12 = Entry(
        bd=0,
        bg="#E9F2FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_12.place(
        x=34.0,
        y=96.00000000000006,
        width=402.0,
        height=23.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buscar_datos(entry_12.get()),
        relief="flat"
    )
    button_8.place(
        x=476.0,
        y=96.00000000000006,
        width=100.0,
        height=25.0
    )

    canvas.create_text(
        35.0,
        77.00000000000006,
        anchor="nw",
        text="LOAD DATA",
        fill="#000000",
        font=("Roboto SemiBold", 12 * -1)
    )

    canvas.create_rectangle(
        24,
        129.00000000000006,
        576.0,
        131.00000000000006,
        fill="#B1D9FF",
        outline="")

def eliminar_gui(window, id: str, canvas):
    # Eliminar todos los widgets de la ventana
    for widget in window.winfo_children():
        if widget != canvas:
            widget.destroy()

    canvas.delete("all")

    if id == "":
        gui.crear_gui(canvas, window)
    elif id == "1":
        gui1.crear_gui(canvas, window)
    elif id == "3":
        gui3.crear_gui(canvas, window)
    elif id == "4":
        gui4.crear_gui(canvas, window)