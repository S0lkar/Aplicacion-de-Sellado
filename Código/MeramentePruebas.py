from Estampillado import Campo, Sello, Estampar_Manual, Estampar_Auto

# ---------------- Definimos las propiedades del sello ----------------
S = Sello("Sello.png", (5,5,5,5), (0,0,255))
S.addCampo(Campo(28, 36, "times", 25, "Hola:", "________"))
S.addCampo(Campo(28, 76, "times", 25, "Adios:", "260€"))

Estampar_Manual("TFG.pdf", 15, S, (200, 100), (150, 100), "TFG_Estampado.pdf")