
import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
from Estampillado import Campo, Sello, Estampar_Manual, Estampar_Auto


def Test():
    global v2
    inp = inputtxt.get(1.0, "end-1c")
    inputtxt.delete("1.0", "end") # !!!!!!!!!!!! para eliminar texto
    v2.destroy()
    v2 = v1.pdf_view(root, pdf_location=r"TFG_Estampado.pdf", width=70, height=100)
    v2.pack(side=tk.LEFT)
    print(inp)

def browseDirectory():
    filename = filedialog.askdirectory(initialdir="/",
                                          title="Select a File",
                                          )
    # Change label contents
    label_file_explorer.configure(text="Directory Opened: " + filename)

def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      ""
                                                      "*.*")))
    print(filename)

def Nuevo_PDF():
    window = tk.Tk()
    # Set window title
    window.title('Abrir PDF')
    # Set window size
    window.geometry("500x500")
    # Set window background color
    window.config(background="white")
    # Create a File Explorer label
    label_file_explorer = tk.Label(window,
                                text="File Explorer using Tkinter",
                                width=100, height=4,
                                fg="blue")
    button_explore = tk.Button(window,
                            text="Browse Files",
                            command=browseFiles)
    button_exit = tk.Button(window,
                         text="Exit",
                         command=window.destroy)
    # Grid method is chosen for placing
    # the widgets at respective positions
    # in a table like structure by
    # specifying rows and columns
    label_file_explorer.grid(column=1, row=1)
    button_explore.grid(column=1, row=2)
    button_exit.grid(column=1, row=3)
    # Let the window wait for any events
    window.mainloop()

# Esto no se va a usar, vaya
def savePDF():
    files = [('All Files', '*.*'),
            ('Text Document', '*.txt')]
    file = tk.filedialog.asksaveasfile(filetypes=files)


# ################## Código de la GUI ####################
"""
La libreria no funciona y hay que hacerle dos apaños:
pix1.tobytes("ppm") -> Soluciona el problema de las imagenes
get_pixmap() -> Soluciona lo del pixmap
"""

# 720 es el medio de la ventana a la derecha
root = tk.Tk()
root.title("Estampillado de PDFs")
root.geometry("900x600")
menubar = tk.Menu(root) # https://docs.hektorprofe.net/python/interfaces-graficas-con-tkinter/widget-menu/
root.config(menu=menubar)  # Lo asignamos a la base
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Archivo", menu=filemenu)
filemenu.add_command(label="Nuevo", command=browseFiles)
filemenu.add_command(label="Abrir")
filemenu.add_command(label="Guardar", command=savePDF)
filemenu.add_command(label="Cerrar")
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)

inputtxt = tk.Text(root, height = 2, width = 20)
inputtxt.insert(tk.INSERT, "Write Something About Yourself")
#inputtxt.pack(side=tk.RIGHT)
inputtxt.place(x=670,y=50)

v1 = pdf.ShowPdf()
v2 = v1.pdf_view(root, pdf_location = r"TFG.pdf", width = 70, height=100)

#v2.place(x=10,y=50)
v2.pack(side=tk.LEFT)
lbl = tk.Label(root, text = "Texto: ")
lbl.place(x=620, y=53)

B = tk.Button(root, text ="Compilar sello", command=Test)
B.place(x=700, y=20)
root.mainloop()