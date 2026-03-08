#pip install tabulate
from tabulate import tabulate
#pip install matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class Celdas:
    parentxy = [-1,-1]
    gn = 0
    fn = -1
    visitada = False

Mapa = [[1,1,0,1,2,1,0,0,1,1],
        [1,1,1,1,2,0,2,1,1,0],
        [0,1,0,4,1,1,3,1,1,1],
        [1,0,1,1,0,2,1,1,2,0],
        [1,1,5,0,1,1,0,1,1,1],
        [1,1,2,0,1,0,1,4,1,1],
        [0,0,1,0,3,1,2,1,1,1],
        [1,1,1,2,1,1,1,1,3,0],
        [1,1,1,0,0,1,0,0,1,1],
        [1,1,1,1,3,1,1,1,2,1]]

MapaVisual = [["Y / X",1,2,3,4,5,6,7,8,9,10]]
y_guia = 0
for fila in Mapa:
    y_guia = y_guia + 1
    filavisual = [y_guia]
    for columna in fila:
        if columna == 0:
            filavisual.append("X")
        else:
            filavisual.append(columna)
    MapaVisual.append(filavisual)

def xyValido(xyString):
    while True:
        try:
            XYcoord = int(input("Ingresa " + xyString + ": "))
            if XYcoord < 1 or XYcoord > 10:
                print("la coordenada " + xyString + " debe de ser un numero entre 1 y 10")
            else:
                return XYcoord
        except ValueError:
            print("La coordenada " + xyString + " debe de ser un numero entero")

def casilla_Valida(ini_fin):
    while True:
        print("Mapa: ")
        print(tabulate(MapaVisual, tablefmt="grid"))
        print("Casilla de " + ini_fin + ": ")
        xCoord = xyValido("X")
        yCoord = xyValido("Y")
        casilla = [yCoord-1, xCoord-1]
        if Mapa[casilla[0]][casilla[1]] == 0:
            print("Casilla bloqueada")
        else:
            return casilla

inicio = casilla_Valida("inicio")
meta = casilla_Valida("meta")
while meta == inicio:
    print("La meta tiene que ser diferente a la casilla inicial")
    meta = casilla_Valida("meta")
buscando = True
celda_Actual = inicio
por_Visitar = []
celda = []
movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
for fila in Mapa:
    datos = []
    for columna in fila:
        datos.append(Celdas())
    celda.append(datos)

def aScore(X, Y):
    costo = celda[celda_Actual[0]][celda_Actual[1]].gn + Mapa[X][Y]
    euristica = abs(meta[0] - X) + abs(meta[1] - Y)
    return([costo, costo + euristica])

celda[inicio[0]][inicio[1]].parentxy = inicio
por_Visitar.append(inicio)

vuelta = 0
while buscando:
    vuelta = vuelta + 1
    minFN = celda[celda_Actual[0]][celda_Actual[1]].fn
    indice = 0
    indice_menor = 0
    for coord in por_Visitar:
        if celda[coord[0]][coord[1]].fn < minFN:
            minFN = celda[coord[0]][coord[1]].fn
            indice_menor = indice
        indice = indice +1
    celda_Actual = por_Visitar.pop(indice_menor)

    celda[celda_Actual[0]][celda_Actual[1]].visitada = True

    for mov in movimientos:
        newX = celda_Actual[0] + mov[0]
        newY = celda_Actual[1] + mov[1]
        #Si coordenadas dentro de la cuadricula
        if newX >= 0 and newX < 10 and newY >= 0 and newY < 10:
            #Si celda no esta bloqueada o fue visitada
            if Mapa[newX][newY] > 0 and celda[newX][newY].visitada == False:
                newXY = [newX, newY]
                if newXY == meta:
                    celda[newX][newY].parentxy = celda_Actual
                    buscando = False
                else:
                    GN_FN = aScore(newX, newY)
                    GN = GN_FN[0]
                    FN = GN_FN[1]
                    if celda[newX][newY].fn == -1 or FN < celda[newX][newY].fn:
                        celda[newX][newY].fn = FN
                        celda[newX][newY].gn = GN
                        celda[newX][newY].parentxy = celda_Actual
                        if newXY not in por_Visitar:
                            por_Visitar.append(newXY)

print("El camino es:")
camino = [[meta[1] + 1, meta[0]+1]]
caminoPLT = [meta]
celda_Actual = meta
while celda[celda_Actual[0]][celda_Actual[1]].parentxy != inicio:
    coordPre = celda[celda_Actual[0]][celda_Actual[1]].parentxy
    celdaCorregida = [coordPre[1] + 1, coordPre[0] + 1]
    camino.append(celdaCorregida)
    caminoPLT.append(coordPre)
    celda_Actual = celda[celda_Actual[0]][celda_Actual[1]].parentxy
camino.append([inicio[1] + 1, inicio[0] + 1])
caminoPLT.append(inicio)
camino.reverse()
print(camino)


XGrid = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
YGrid = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

MapaFinal = []
for x in range(10):
    filaPLT = []
    for y in range(10):
        if Mapa[x][y] == 0:
            filaPLT.append(-1)
        elif [x,y] in caminoPLT:
            filaPLT.append(1)
        else:
            filaPLT.append(0)
    MapaFinal.append(filaPLT)

colors = [(1, 0, 0), (1, 1, 1), (0, 1, 0)]
cmap_name = 'mapa_Pro'
cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)

fig, ax = plt.subplots()
im = ax.imshow(MapaFinal, cmap = cmap)

# Show all ticks and label them with the respective list entries
ax.set_xticks(range(len(YGrid)), labels=YGrid)
ax.set_yticks(range(len(XGrid)), labels=XGrid)

# Loop over data dimensions and create text annotations.
for i in range(len(XGrid)):
    for j in range(len(YGrid)):
        text = ax.text(j, i, MapaVisual[i+1][j+1],
                       ha="center", va="center", color="black")
        
ax.set_title("Ruta Encontrada")
fig.tight_layout()
plt.show()