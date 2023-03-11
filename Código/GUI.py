
import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
from tkinter import filedialog
from PIL import ImageTk, Image
from Estampillado import Campo, Sello, Estampar_Manual, Estampar_Auto, Marca_de_Agua, PNG_a_PDF
from tkinter import *
from tkinter import colorchooser
import os


# --- Funciones auxiliares y variables globales ---
S = Sello("Sello.png", (0,0,0,0))
S.addCampo(Campo())
img = None
nCampo = 0

Input = ""
Output = ""
Ref = ""
opc = 1 # == 1 para manual, == 2 para automatico
nom_Imagen = ""
v1 = None
v2 = None

# ---------- Funciones asociadas al menú de creación de Sellos -------------

def RefrescaDatos(nom, tamB, nCam, posX, posY, Fuente, TamFuente, Texto, Val):
    global S
    S.Name = nom
    S.scaleBorde(tamB)
    S.Campos[nCam].setPosX(posX)
    S.Campos[nCam].setPosY(posY)
    S.Campos[nCam].setFuente(Fuente)
    S.Campos[nCam].setTamFuente(TamFuente)
    S.Campos[nCam].setTexto(Texto)
    S.Campos[nCam].setVal(Val)

def Actualiza_nCampo(val, Borde, Cmp, PosX, PosY, Fuente, TamFuente, Texto, Valor):
    global nCampo, S
    nCampo = val
    if val >= len(S.Campos):
        S.addCampo(Campo()) # Si se intenta acceder a un campo que aún no se había creado, se añade
    Refrescar_Componentes(val, Borde, Cmp, PosX, PosY, Fuente, TamFuente, Texto, Valor)

# Refresca el canvas con el sello actual
def Actualizar_Canvas(canvas, nom, tamB, nCam, posX, posY, Fuente, TamFuente, Texto, Val):
    global img, S
    RefrescaDatos(nom, tamB, nCam, posX, posY, Fuente, TamFuente, Texto, Val)
    S.compileSello(True, "temp.png")
    img = tk.PhotoImage(file="temp.png")
    canvas.create_image(20, 20, anchor=NW, image=img)
    os.remove("temp.png")

# Refresca el canvas con los datos que ya están cargados
def Recargar_Canvas(canvas):
    global img, S
    S.compileSello(True, "temp.png")
    img = tk.PhotoImage(file="temp.png")
    canvas.create_image(20, 20, anchor=NW, image=img)
    os.remove("temp.png")

def guardarSello(texto_nom):
    filename = filedialog.askdirectory(initialdir="/", title="Selecciona una carpeta")
    S.guardarSello(filename + "/" + texto_nom + ".txt")

def abrirSello(canvas, Borde, Campo, PosX, PosY, Fuente, TamFuente, Texto, Valor):
    global S, nCampo
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      ""
                                                      "*.*")))
    S.leerSello(filename)
    Recargar_Canvas(canvas)
    Refrescar_Componentes(0, Borde, Campo, PosX, PosY, Fuente, TamFuente, Texto, Valor)

def ResetSello():
    global S
    S = Sello()
    # Tendría que resetear los campos del sello igualmente

def cambiarcolor():
    color = colorchooser.askcolor()
    S.setColor(color[0])

# Pone el contenido del campo "iCampo" en los componentes
def Refrescar_Componentes(iCampo, Borde, Campo, PosX, PosY, Fuente, TamFuente, Texto, Valor):
    global S
    Borde.delete(0, END)
    Borde.insert(0, S.Borde[0])

    Campo.delete(0, END)
    Campo.insert(0, str(iCampo))
    PosX.delete(0, END)
    PosX.insert(0, S.Campos[iCampo].PosX)
    PosY.delete(0, END)
    PosY.insert(0, S.Campos[iCampo].PosY)
    TamFuente.delete(0, END)
    TamFuente.insert(0, S.Campos[iCampo].TamFuente)
    Fuente.delete("1.0", END)
    Fuente.insert(tk.INSERT, S.Campos[iCampo].Fuente)
    Texto.delete("1.0", END)
    Texto.insert(tk.INSERT, S.Campos[iCampo].Texto)
    Valor.delete("1.0", END)
    Valor.insert(tk.INSERT, S.Campos[iCampo].Val)


# ---------- Funciones asociadas al menú de gestión de PDFs -------------

def SellarManual(root, pos, tam, numPag):
    global S, v1, v2, Input, Output, Ref

    Estampar_Manual(os.path.basename(Input).split('/')[-1], numPag, S, pos, tam, Output) # Estampa el PDF
    # ------ Actualizacion del viewer para ver los cambios ------
    Folder = os.path.dirname(Output)
    Fichero = os.path.basename(Ref).split('/')[-1]
    Ref = Folder + '/' + Fichero
    v2.destroy()
    v1.img_object_li.clear()
    v2 = v1.pdf_view(root, pdf_location=Ref, width=70, height=100)
    v2.pack(side=tk.LEFT)

def SellarAuto(root, pos, tam, numPag):
    global S, Ref, Output, Input, v1, v2
    Estampar_Auto(Input, S, pos, tam, numPag, Output)
    # ------ Actualizacion del viewer para ver los cambios ------
    Fichero = os.path.basename(Ref).split('/')[-1]  # nombre del PDF de referencia
    Ref = Output + "/" + Fichero
    v2.destroy()
    v1.img_object_li.clear()
    v2 = v1.pdf_view(root, pdf_location=Ref, width=70, height=100) # Ref actualizada
    v2.pack(side=tk.LEFT)

def seleccionarPDF(root, opcSellado):
    global Input, Output, Ref, opc
    opc = opcSellado
    if opcSellado == 1: # Manual
        Input = filedialog.askopenfilename(initialdir="/", title="Seleccione el PDF a sellar",
                                              filetypes=(("all files", "" "*.*"), ("Text files", "*.txt*")))
        Output = filedialog.askdirectory(initialdir="/", title="Seleccione la carpeta destino")
        Ref = Input
        Output = Output + "/" + os.path.basename(Input).split('/')[-1]

    elif opcSellado == 2: # Automático
        Input = filedialog.askdirectory(initialdir="/", title="Seleccione la carpeta a sellar")
        Output = filedialog.askdirectory(initialdir="/", title="Seleccione la carpeta destino")
        Ref = filedialog.askopenfilename(initialdir="/", title="Seleccione un PDF de referencia para sellar",
                                           filetypes=(("all files", "" "*.*"), ("Text files", "*.txt*")))

    root.destroy()


# -- Marcas de agua --
def seleccionarMarcadeAgua():
    Input = filedialog.askopenfilename(initialdir="/", title="Seleccione el PDF",
                                              filetypes=(("all files", "" "*.*"), ("Text files", "*.txt*")))
    Img = filedialog.askopenfilename(initialdir="/", title="Seleccione la imagen",
                                       filetypes=(("all files", "" "*.*"), ("Text files", "*.txt*")))
    Output = filedialog.askdirectory(initialdir="/", title="Seleccione la carpeta destino")
    Output = Output + "/" + os.path.basename(Input).split('/')[-1] # Se llamará igual que su versión no-Marcada

    Nombre_temp = os.path.dirname(Img) + "/temp.pdf"

    PNG_a_PDF(Img, Nombre_temp)
    Marca_de_Agua(Input, Nombre_temp, Output)
    os.remove(Nombre_temp)



# ---- Menú del Sello ----
def menu_Sello():
    global S, nCampo
    # --- Ajustes de la ventana ---
    root = tk.Tk()
    root.title("Ajustes del sello")
    root.geometry("825x450")
    # ----- Declaración de los elementos -----
    # --- Menú superior ---
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Archivo", menu=filemenu)
    filemenu.add_command(label="Nuevo", command=ResetSello)
    filemenu.add_command(label="Abrir", command=lambda: abrirSello(canvas, Spin_Borde, Spin_Campo, Spin_PosX, Spin_PosY, inputFuente, Spin_TamF, inputTXT, inputVAL))

    PDF_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Sellar PDF", menu=PDF_menu)
    PDF_menu.add_command(label="Carpeta", command=lambda: seleccionarPDF(root, 2))
    PDF_menu.add_command(label="Individual", command=lambda: seleccionarPDF(root, 1))

    Marca_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Marca de Agua", menu=Marca_menu)
    Marca_menu.add_command(label="Añadir a PDF", command=seleccionarMarcadeAgua)

    # --- Canvas para mostrar la imagen del sello ---
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack(side=tk.LEFT)
    S.addCampo(Campo()) # El campo 0
    Actualizar_Canvas(canvas, "Sello", 0, 0, 0, 0, "times", 0, " ", " ") # Para mostrar el sello default

    # --- Opciones para configuracion global del sello ---
    B = tk.Button(root, text="Visualizar sello", command=lambda: Actualizar_Canvas(canvas, inputNOM.get("1.0", "end-1c"), int(Spin_Borde.get()[:2]), int(Spin_Campo.get()[:2]), int(Spin_PosX.get()[:2]), int(Spin_PosY.get()[:2]), inputFuente.get("1.0", "end-1c"), int(Spin_TamF.get()[:2]), inputTXT.get("1.0", "end-1c"), inputVAL.get("1.0", "end-1c")))
    B.place(x=500, y=20)
    B = tk.Button(root, text="Cambiar color", command=cambiarcolor)
    B.place(x=600, y=20)

    # nombre del archivo
    etiqueta = tk.Label(text="Nombre del sello:")
    etiqueta.place(x=430, y=60)
    inputNOM = tk.Text(root, height=1, width=20)
    inputNOM.insert(tk.INSERT, "Sello")
    inputNOM.place(x=550, y=60)

    filemenu.add_command(label="Guardar", command=lambda: guardarSello(inputNOM.get("1.0", "end-1c")))

    # borde
    Spin_Borde = tk.Spinbox(from_=0, to=50, increment=1, command=lambda: S.scaleBorde(int(Spin_Borde.get()[:2])))
    Spin_Borde.place(x=550, y=90)
    etiqueta = tk.Label(text="Tamaño del borde: ")
    etiqueta.place(x=430, y=89)
    # campo seleccionado
    Spin_Campo = tk.Spinbox(from_=0, to=50, increment=1, state='readonly', command=lambda: Actualiza_nCampo(int(Spin_Campo.get()[:2]), Spin_Borde, Spin_Campo, Spin_PosX, Spin_PosY, inputFuente, Spin_TamF, inputTXT, inputVAL))
    Spin_Campo.place(x=550, y=120)
    etiqueta = tk.Label(text="Campo seleccionado:")
    etiqueta.place(x=430, y=119)

    # --- Opciones para definir campos ---
    #pos X -- Les falta decir cual es cual
    etiqueta = tk.Label(text="Posicion:")
    etiqueta.place(x=430, y=200)
    Spin_PosX = tk.Spinbox(from_=0, to=300, increment=1, command=lambda: S.Campos[nCampo].setPosX(int(Spin_PosX.get()[:2])))
    Spin_PosX.place(x=490, y=200)
    # pos Y
    Spin_PosY = tk.Spinbox(from_=0, to=200, increment=1, command=lambda: S.Campos[nCampo].setPosY(int(Spin_PosY.get()[:2])))
    Spin_PosY.place(x=650, y=200)
    #fuente
    etiqueta = tk.Label(text="Fuente:")
    etiqueta.place(x=430, y=230)
    inputFuente = tk.Text(root, height=1, width=15)
    inputFuente.insert(tk.INSERT, "times")
    inputFuente.place(x=490, y=230)
    #tamaño fuente
    Spin_TamF = tk.Spinbox(from_=0, to=90, increment=1, command=lambda: S.Campos[nCampo].setTamFuente(int(Spin_TamF.get()[:2])))
    Spin_TamF.place(x=650, y=230)
    # texto
    etiqueta = tk.Label(text="Texto:")
    etiqueta.place(x=440, y=290)
    inputTXT = tk.Text(root, height=2, width=30)
    inputTXT.insert(tk.INSERT, "Texto del campo")
    inputTXT.place(x=500, y=285)
    # valor
    etiqueta = tk.Label(text="Valor:")
    etiqueta.place(x=440, y=350)
    inputVAL = tk.Text(root, height=2, width=30)
    inputVAL.insert(tk.INSERT, "Valor del campo")
    inputVAL.place(x=500, y=345)

    root.mainloop()


# ---- Menú del Estampado ----
def menu_Estampado():
    global S, opc, Input, Output, Ref, v1, v2
    root = tk.Tk()
    root.title("Estampillado de PDFs")
    root.geometry("900x600")
    # --- Vista del PDF ---
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(root, pdf_location=Ref, width=70, height=100)
    v2.pack(side=tk.LEFT)
    if opc == 1: # Se eligió estampar de forma manual
        B = tk.Button(root, text="Colocar sello", command=lambda: SellarManual(root, (int(Spin_PosX.get()), int(Spin_PosY.get())), (int(Spin_TamX.get()), int(Spin_TamY.get())), int(Spin_Npag.get())))
        B.place(x=700, y=20)
    else: # Si no, de forma automática
        B = tk.Button(root, text="Colocar sello", command=lambda: SellarAuto(root, (int(Spin_PosX.get()), int(Spin_PosY.get())), (int(Spin_TamX.get()), int(Spin_TamY.get())), int(Spin_Npag.get())))
        B.place(x=695, y=20)

    # Posicion del sello
    # pos X -- Les falta decir cual es cual
    etiqueta = tk.Label(text="Posicion:")
    etiqueta.place(x=710, y=50)
    Spin_PosX = tk.Spinbox(from_=0, to=1000, increment=1)
    Spin_PosX.place(x=590, y=80)
        # pos Y
    Spin_PosY = tk.Spinbox(from_=0, to=1000, increment=1)
    Spin_PosY.place(x=750, y=80)

    # Tamaño del sello
    etiqueta = tk.Label(text="Tamaño:")
    etiqueta.place(x=710, y=120)
    Spin_TamX = tk.Spinbox(from_=0, to=1000, increment=1)
    Spin_TamX.place(x=590, y=150)
    # Tam Y
    Spin_TamY = tk.Spinbox(from_=0, to=1000, increment=1)
    Spin_TamY.place(x=750, y=150)

    # Nº de pagina donde colocarlo
    etiqueta = tk.Label(text="Nº de Pagina:")
    etiqueta.place(x=590, y=190)
    Spin_Npag = tk.Spinbox(from_=0, to=1000, increment=1)
    Spin_Npag.place(x=750, y=190)

    root.mainloop()


if __name__ == "__main__":
    while opc != 0:
        opc = 0
        menu_Sello()
        if opc != 0:
            menu_Estampado()


