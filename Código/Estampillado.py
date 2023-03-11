

from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import fitz     # pip install fitz      pip install PyMuPDF
from PyPDF4 import PdfFileWriter, PdfFileReader # pip install PyPDF4
import PyPDF4


class Campo:
    def __init__(self, PosX = 0, PosY = 0, Fuente = "times", TamFuente = 0, Texto = "", Val = ""):
        self.PosX = PosX
        self.PosY = PosY  # Posición de donde se coloca el campo dentro del sello
        self.Fuente = Fuente # String con el nombre de la fuente
        self.TamFuente = TamFuente # Tamaño de la fuente
        self.Texto = Texto # Texto del campo
        self.Val = Val # Valor del campo. Si es un "sello informativo", se puede dejar vacío
        self.trueFont = ImageFont.truetype(Fuente, TamFuente)

    # --- Métodos para modificar las propiedades de los campos ---
    def setPosX(self, PosX):
        self.PosX = PosX

    def setPosY(self, PosY):
        self.PosY = PosY

    def setTexto(self, Texto):
        self.Texto = Texto

    def setVal(self, Val):
        self.Val = Val

    def setFuente(self, Fuente):
        self.Fuente = Fuente
        self.trueFont = ImageFont.truetype(Fuente, self.TamFuente)

    def setTamFuente(self, TamFuente):
        self.TamFuente = TamFuente
        self.trueFont = ImageFont.truetype(self.Fuente, TamFuente)

class Sello:
    def __init__(self, Name="Sello.png", Borde=(5, 5, 5, 5), Color = (0,0,255), Tam = (300,200)):
        self.Name = Name
        self.Borde = Borde
        self.Color = Color
        self.Tam = Tam
        self.Campos = []

    # --- Métodos para modificar las propiedades del sello ---
    def setName(self, Name):
        self.Name = Name

    def addCampo(self, new_Campo):
        self.Campos.append(new_Campo)

    def deleteCampo(self, indice):
        self.Campos.pop(indice)

    def setBorde(self, Borde):
        self.Borde = Borde

    def scaleBorde(self, Escala):
        self.Borde = tuple([Escala*x for x in (1, 1, 1, 1)])

    def setColor(self, Color):
        self.Color = Color

    def setTam(self, Tam):
        self.Tam = Tam

    # Método para cargar la imagen asociada al sello. Devuelve la imagen, y si Guardar==true, guardará la imagen con
    # el nombre especificado en "temp_Name" o, si no se indicó, con el nombre del propio sello.
    def compileSello(self, Guardar, temp_Name = ""):
        img = Image.new('RGB', self.Tam, (255, 255, 255)) # Fondo blanco en el sello, del tamaño especificado
        img = ImageOps.expand(img, border=self.Borde, fill=self.Color) # Borde si lo hubiera
        I1 = ImageDraw.Draw(img)
        for c in self.Campos:
            I1.text((c.PosX, c.PosY), c.Texto + c.Val, font=c.trueFont, fill=self.Color)

        if Guardar: # Si no se requiere de compilar para guardar, no se hará
            if temp_Name != "": # Para el caso de estampar, hacerlo con otro nombre
                img.save(temp_Name)
            else:
                img.save(self.Name)

        return img

    # Lee el sello del fichero especificado, borrando el contenido anterior
    def leerSello(self, Filename):
        file = open(Filename, 'r', encoding="utf-8")
        l = file.readlines()
        self.Name = l[0][:-1] # -1 para quitar el salto de línea al final
        self.Borde = tuple(map(int, l[1].split(',')))
        self.Color = tuple(map(int, l[2].split(',')))
        self.Tam = tuple(map(int, l[3].split(',')))
        self.Campos = [] # Quita los campos antiguos, si los hubiera
        cont = 4
        while cont < len(l): # .split('\n')[0] -> Para no leer el último salto de linea
            self.addCampo(Campo(int(l[cont]), int(l[cont+1]), l[cont+2].split('\n')[0], int(l[cont + 3]), l[cont+4].split('\n')[0], l[cont+5].split('\n')[0]))
            cont += 6
        file.close()
        pass

    # Guarda el sello en el nombre de fichero especificado. Si el fichero contenía un sello, lo sobreescribe.
    def guardarSello(self, Filename):
        file = open(Filename, 'w+', encoding="utf-8")
        file.write(self.Name + '\n' + str(flatten(self.Borde)) + '\n' + str(flatten(self.Color)) + '\n' + str(flatten(self.Tam)))
        for c in self.Campos:
            if c.Texto == "": # Colocamos un espacio para que el efecto visual sea el mismo pero permita leer sellos guardados
                c.Texto = " "
            if c.Val == "":
                c.Val = " "
            file.write('\n' + str(c.PosX) + '\n' + str(c.PosY) + '\n' + c.Fuente + '\n' + str(c.TamFuente) + '\n' + c.Texto + '\n' + c.Val)
        file.close()
        print(Filename)
        pass

# Función auxiliar para "aplanar" tuplas en listas
def flatten(o):
    if not isinstance(o, (list, tuple, dict)):
        return str(o)
    elif isinstance(o, (list, tuple)):
        return ",".join(flatten(e) for e in o)
    elif isinstance(o, dict):
        return ",".join(e + ": " + flatten(o[e]) for e in o)

# Estampa el sello dentro del fichero "inputNombre" en la página "numPag", con el sello "S" en la posición "pos",
# con un tamaño de "tam" (o el tamaño del sello si tam es (0,0) y guarda el resultado en "outputNombre".
def Estampar_Manual(inputNombre, numPag, S, pos, tam, outputNombre):
    S.compileSello(True, "Sello_" + inputNombre[:-4] + ".png") # Guardamos el sello a aplicar
    img = open("Sello_" + inputNombre[:-4] + ".png", "rb").read() # Y obtenemos su ruta para emplearlo
    if tam == (0, 0):
        tam = tuple(map(lambda i, j: i + j, S.Tam, S.Borde)) # Tamaño junto al borde del sello
    TAM = tuple(map(lambda i, j: i + j, tam, pos)) # Para deducir el recuadro final del sello en la página
    image_rectangle = fitz.Rect(pos, TAM)
    file_handle = fitz.open(inputNombre)
    first_page = file_handle[numPag] # Abrimos la página deseada
    first_page.insert_image(image_rectangle,stream=img,xref=0) # Y colocamos el sello donde corresponde
    file_handle.save(outputNombre) # Guardamos el PDF modificado

# Dada la carpeta "inputCarpeta", un sello "S", una posición "pos", tamaño de sello "tam", número de página "numPag" y
# la carpeta destino "outputCarpeta", sella todos los PDFs que encuentre con esas condiciones y los guarda en
# la carpeta de destino
def Estampar_Auto(inputCarpeta, S, pos, tam, numPag, outputCarpeta):
    S.compileSello(True, "SelloGrupal_" + S.Name + ".png")
    img = open("SelloGrupal_" + S.Name + ".png", "rb").read()
    if tam == (0, 0):
        tam = tuple(map(lambda i, j: i + j, S.Tam, S.Borde)) # Tamaño junto al borde del sello
    TAM = tuple(map(lambda i, j: i + j, tam, pos)) # Para deducir el recuadro final del sello en la página
    image_rectangle = fitz.Rect(pos, TAM)

    listado = [f for f in os.listdir(inputCarpeta) if f.endswith('.pdf')] # Listado de PDFs encontrados en la carpeta
    for PDF in listado:
        file_handle = fitz.open(inputCarpeta + "/" + PDF)
        first_page = file_handle[numPag]
        first_page.insert_image(image_rectangle, stream=img, xref=0)
        file_handle.save(outputCarpeta + "/" + PDF)
    pass

# Dado el pdf "input_pdf", un pdf con la imagen a usar de marca de agua ("watermark") y el PDF de destino ("output_pdf"),
# marca todas las páginas del pdf solicitado y guarda el resultado en la dirección de output especificada
def Marca_de_Agua(input_pdf, watermark, output_pdf):
    PyPDF4.PdfFileReader(input_pdf)
    watermark_instance = PdfFileReader(watermark)
    watermark_page = watermark_instance.getPage(0)
    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)

# Toma la imagen en "rutaIN", y la transforma a PDF en "rutaOUT"
def PNG_a_PDF(rutaIN, rutaOUT):
    image_1 = Image.open(rutaIN)
    im_1 = image_1.convert('RGB')
    im_1.save(rutaOUT)
