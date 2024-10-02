from tkinter import Tk, Canvas
import gui

windows = Tk("CREATE")
windows.title("Don Baraton's Administrator GUI")

windows.geometry("600x624+{}+{}".format(int(windows.winfo_screenwidth() / 2 - 300), int(windows.winfo_screenheight() / 2 - 312)))

windows.configure(bg ="#FFFFFF")



canvas = Canvas(
    windows,
    bg = "#FFFFFF",
    height = 624,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

gui.crear_gui(canvas, windows)

windows.resizable(False, False)
windows.mainloop()

