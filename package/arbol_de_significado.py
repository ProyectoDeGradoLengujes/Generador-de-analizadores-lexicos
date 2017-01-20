import sys
import graphviz as graph

dicOperaciones = {}
pilaNodos = []
pilaOperaciones = []
pilaParentesis = []
numNodo = 0
pareja = 0

"""
 Crea conexiones para grafos unidireccionales
"""
def make_link (G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    return G

"""
Recibe el arbol de significado y el nombre que tendra el archivo
Utiliza la libreria graphviz para pintar el arbol de significado
"""
def dibujarArbol(G,etiqueta):
    g2 = graph.Digraph(format='png')
    for node1 in G:
        for node2 in G[node1]:
            g2.node(str(node1))
            g2.node(str(node2))
            g2.edge(str(node1),str(node2))
    filename = g2.render(filename='img/g'+ etiqueta)

def manejoOperaciones(token,arbol):
    dicbinarias = {'|':op_or,'fin':0}    
    global pareja
    pareja = 0
    if token in dicbinarias:
        if len(pilaOperaciones) <= 0:
            pilaOperaciones.append(token)
            pilaNodos.append(numNodo)
            return
        else:
            operacion = dicOperaciones[pilaOperaciones.pop()]
            operacion(arbol)
            pilaOperaciones.append(token)
            pilaNodos.append(numNodo)
    else:
        pilaOperaciones.append(token)
        pilaNodos.append(numNodo)
        operacion = dicOperaciones[token]
        operacion(arbol)

def op_or(arbol):
    global numNodo
    nodo1 = numNodo
    numNodo += 1
    nodo2 = pilaNodos.pop()
    make_link(arbol, numNodo, nodo1)
    make_link(arbol, numNodo, nodo2)
    make_link(arbol, numNodo, '|')
    #print ("operacion or")

def op_unaria(arbol):
    global pareja
    nodo1 = pilaNodos.pop()
    op = pilaOperaciones.pop()
    t = len(arbol[nodo1])
    if t == 2:
        make_link(arbol, nodo1 - 1, op)
    else:
        make_link(arbol, nodo1, op)
    pareja += 1    
    #print ("operacion super mas")

def parentesisA(arbol):
    pilaOperaciones.pop()
    nodo = pilaNodos.pop()
    pilaParentesis.append(nodo)
    #print ("parentesis que abre")

def parentesisB(arbol):
    op = pilaOperaciones.pop()
    pilaNodos.pop()
    """
    verifica que no existan operaciones pendientes dentro 
    de los parentesis para realizarlas antes de cerrar los parentesis
    """
    if len(pilaParentesis) <= 1:#identifica perentesis anidados
        while len(pilaOperaciones) > 0:
            operacion = dicOperaciones[pilaOperaciones.pop()]
            operacion(arbol)
    global numNodo
    global pareja
    """
    Incluye un nuevo nodo con los parentesis para hacer refencia 
    a la expresion regular que esta denrto de los parentesis
    """
    nodo1 = numNodo
    numNodo += 1
    make_link(arbol, numNodo, '(')
    make_link(arbol, numNodo, op)
    make_link(arbol, numNodo, numNodo - 1)
    #Une la expresion regular del parentesis con el resto del arbol
    
    nodo2 = pilaParentesis.pop()
    if nodo2 != 0:
        numNodo += 1
        make_link(arbol, numNodo, nodo1+1)
        if len(pilaParentesis) == 0: #identifica perentesis anidados
            make_link(arbol, numNodo, nodo2)
        pareja += 1


"""
Recibe una cadena que contiene la definicion del ER y una lista con la posicion de los parentesis
Retorna el arbol de significado
"""
def hacerArbol(ER):
    global numNodo
    global pareja
    global dicOperaciones
    dicOperaciones = {'*':op_unaria,'+':op_unaria,'|':op_or,'(':parentesisA,')':parentesisB,'fin':0}
    arbol = {}
    i = 0
    while i < len(ER):
        token = ER[i]
        #busqueda en el diccionario de la funcion que desarrolla la funcion
        if token in dicOperaciones:
            manejoOperaciones(token,arbol)
        else:
            #generacion de la relacion simple nodo - token
            numNodo += 1
            make_link(arbol, numNodo, token)
            pareja += 1
        i += 1
        #operacion and
        if pareja == 2:
            numNodo += 1
            make_link(arbol, numNodo, numNodo-1)
            make_link(arbol, numNodo, numNodo-2)
            pareja -= 1
        """
        se excluye el unico operador que no altera el arbol para 
        dibujar solamente los cambios del arbol
        """
        if token != '(':
            dibujarArbol(arbol,str(i))  
    
    if 0 in arbol[numNodo]:
        del arbol[numNodo]
    manejoOperaciones('fin',arbol)   
    return arbol
    
"""
Lee el archivo de entrada y delega el procesamiento por fases.
    1) Crear el arbol de significado
    2) Dibuja el arbol de significado
    4) Recorre el arbol de significado
"""
def arbolSignificado():
    fileER = open('test/prueba.txt', 'r')
    for ER in fileER:
        ###print "caso --->", i + 1
        ER.strip()
        ER = list(map(str, ER))
        # ER almacenara una lista con el orden en que deben ser operados los parentesis
        arbolFinal = hacerArbol(ER)
        print (arbolFinal)
        dibujarArbol(arbolFinal, "finals")
        return arbolFinal

arbolSignificado()