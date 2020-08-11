# Trabajo realizado por Ivan Lopez de Munain Quintana

from collections import defaultdict

class Monticulo():

    def __init__(self):
       self.array = [] #array [ nodo v, key[v] ]
       self.tamano = 0 #tamanno
       self.posicion = [] #posicion

    #intercambiar dos nodos en el monticulo
    def intercambioNodos(self, a, b):
       t = self.array[a]
       self.array[a] = self.array[b]
       self.array[b] = t


    def constrMonticulo(self, indice):
       min = indice
       izq = 2 * indice + 1 #para tener en cuenta el cero
       dch = 2 * indice + 2

       if izq < self.tamano and self.array[izq][1] < self.array[min][1]:
           min = izq

       if dch < self.tamano and self.array[dch][1] < self.array[min][1]:
           min = dch

       #si no coincide hay que reorganizar el monticulo
       if min != indice:

           # Intercambio de posiciones
           self.posicion[ self.array[min][0] ] = indice
           self.posicion[ self.array[indice][0] ] = min

           # Intercambio de  nodos
           self.intercambioNodos(min, indice)
           #recursivo hasta comprobar que se cumple la propiedad de monticulo
           self.constrMonticulo(min)

    #extraccion del nodo minimo del monticulo
    def minimo(self):

       # guardamos el elemento raiz que tiene la menor distancia
       raiz = self.array[0]

       #lo remplazamos con el ultimo que es el que mayor distancia tiene para que luego se reordene
       ultimoNodo = self.array[self.tamano - 1]
       self.array[0] = ultimoNodo

       #actualizamos las posiciones
       self.posicion[ultimoNodo[0]] = 0
       self.posicion[raiz[0]] = self.tamano - 1

       #reducimos el tamanno del monticulo para saber que nodos han sido ya incorporados al MST
       self.tamano -= 1
       #reorganizamos el monticulo
       self.constrMonticulo(0)

       return raiz

    def esVacio(self):
        return True if self.tamano == 0 else False

    def filtrarArriba(self, v, key):

       i = self.posicion[v]
       # actualizar el valor de la distancia
       self.array[i][1] = key

       while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
           # intercambiar posiciones del nodo con su padre
           self.posicion[ self.array[i][0] ] = (i-1)//2
           self.posicion[ self.array[(i-1)//2][0] ] = i
           self.intercambioNodos(i, (i - 1)//2 )
           i = (i - 1) // 2 #movemos el indice al padre

    #ver si el nodo v aun no ha sido seleccionado
    def estaMonticulo(self, v):

       if self.posicion[v] < self.tamano:
           #se encuentra en el monticulo
           return True
       #no se encuentra en el monticulo
       return False


def printArr(mstConstruido, n,key):
    z=0
    for i in range(1, n):
        print( "Arista que une a % d - % d, longitud: % d" % (mstConstruido[i], i,key[i]) )
        z+=key[i]
    print("Distancia total:", z)


class Prim():

    def __init__(self, N):
       #numero de nodos
       self.N = N
       #defaultdict se comporta igual que un diccionario normal, la diferencia radica en que con defaultdict si la llave no se encuentra
       #en el diccionario no se genera un KeyError, se genera una nueva entrada del tipo en este caso list.
       self.graph = defaultdict(list)


    def ponerNodo(self, origen, destino, dist):

       #insert(index,elemento), se inserta en el indice cero asi no es
       #necesario conocer la longitud final, el resto de elementos se desplazarian sumando uno en el indice
       self.graph[origen].insert(0, [destino, dist]) #origen es la clave y a ella esta asociada [destino,distancia]
       #grafo no dirigido, por eso se introduce una segunda vez
       self.graph[destino].insert(0, [origen, dist])




    def primMST(self):

       #obtener el numero de nodos
       N = self.N
       # clave asociada a cada nodo para ordenar el monticulo
       key = []
       #mstConstruido sirve para almacenar el MST construido, representa las aristas que conectan el nodo i con mstConstruido[i]
       mstConstruido = []
       #creacion del monticulo
       monticulo = Monticulo()

       #Inicializacion del monticulo con todos los vertices.
       #Valor de las claves igual a infinito
       for v in range(N):
           mstConstruido.append(-1)
           key.append(9999999)
           monticulo.array.append( [v, key[v]] )
           monticulo.posicion.append(v)

       #para extraer primero el nodo raiz escogido
       key[0] = 0
       monticulo.tamano = N;

       #Mientras haya nodos en el monticulo seguimos
       while monticulo.esVacio() == False:
           #obtencion del nodo con menor distancia
           nodoMin = monticulo.minimo() #nodoMin=[v,key[v]]
           u = nodoMin[0] #u = nodo v

           #recorrer todos los vertices adyacentes al nodo u viendo sus distancias
           #recordar que graph se trata de un diccionario en el que la clave es un nodo origen y su valor una lista [nodo destino, distancia] -> [recorrido[0],recorrido[1]]
           for recorrido in self.graph[u]:

               v = recorrido[0] #obtenemos el nodo destino

               #comprobar si el nodo v se encuentra aun en el monticulo y si la distancia del nodo u a v es menor que la clave almacenada en key[v]
               #(recordar que las hemos inicializado a un valor muy alto)
               if monticulo.estaMonticulo(v) and recorrido[1] < key[v]:
                   key[v] = recorrido[1]  #almacenamos la longitud de la arista que une a los nodos v y u
                   mstConstruido[v] = u

                   # actualizacion del monticulo
                   monticulo.filtrarArriba(v, key[v])

       printArr(mstConstruido, N,key)





grafo = Prim(9)
grafo.ponerNodo(0, 1, 4)
grafo.ponerNodo(0, 7, 8)
grafo.ponerNodo(1, 2, 8)
grafo.ponerNodo(1, 7, 11)
grafo.ponerNodo(2, 3, 7)
grafo.ponerNodo(2, 8, 2)
grafo.ponerNodo(2, 5, 4)
grafo.ponerNodo(3, 4, 9)
grafo.ponerNodo(3, 5, 14)
grafo.ponerNodo(4, 5, 10)
grafo.ponerNodo(5, 6, 2)
grafo.ponerNodo(6, 7, 1)
grafo.ponerNodo(6, 8, 6)
grafo.ponerNodo(7, 8, 7)
grafo.primMST()

#otro ejemplo
#grafo = Prim(5)
#grafo.ponerNodo(0,1, 2)
#grafo.ponerNodo(0, 3, 6)
#grafo.ponerNodo(1, 2, 3)
#grafo.ponerNodo(1, 3, 8)
#grafo.ponerNodo(1, 4, 5)
#grafo.ponerNodo(2, 4, 7)
#grafo.ponerNodo(3, 4, 9)
#print(grafo.graph)
#grafo.primMST()
