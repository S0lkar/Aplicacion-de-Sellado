
from Estampillado import Campo, Sello, Estampar_Manual, Estampar_Auto, Marca_de_Agua, PNG_a_PDF

# ---------------- Definimos las propiedades del sello ----------------
S = Sello("Sello.png", (5,5,5,5), (0,0,255))
S.addCampo(Campo(28, 36, "times", 25, "Hola:", "________"))
S.addCampo(Campo(28, 76, "times", 25, "Adios:", "260€"))

# ---------------- Mostramos el resultado del sello ----------------
img = S.compileSello(False)

Estampar_Manual("Pagina.pdf", 0, S, (200, 100), (150, 100), "Estampado.pdf")
S.Campos[0].setTexto("Hola?:")

S.scaleBorde(0) # equivalente a S.setBorde((0,0,0,0))
Estampar_Auto("./PDFs_a_pasar", S, (200, 100), (150, 100), 0, "./PDFs_listos")
print("Terminado ")

# ---------------- Guardamos y cargamos el sello ----------------
S.guardarSello("Sello_Prueba.txt")
Saux = Sello()
Saux.leerSello("Sello_Prueba.txt")
Saux.deleteCampo(1)
Saux.guardarSello("leidoYcopiado.txt")


# ---------------- Añadir marca de agua a un PDF ----------------
"""
En el primer caso, 'car.png' es de un tamaño muy grande y la marca de agua no lo mostrará entero.
En el segundo caso, redimensioné la imagen a 480x240 y el PDF resultante si lo muestra al completo.
"""
PNG_a_PDF('./PDFs_a_pasar/car.png', './PDFs_a_pasar/car.pdf')
Marca_de_Agua('./TFG.pdf', './PDFs_a_pasar/car.pdf', './PDFs_a_pasar/Otro/TFG_con_MdA.pdf')

PNG_a_PDF('./PDFs_a_pasar/carpeque.png', './PDFs_a_pasar/carpeque.pdf')
Marca_de_Agua('./TFG.pdf', './PDFs_a_pasar/carpeque.pdf', './PDFs_a_pasar/Otro/TFG_con_MdA2.pdf')