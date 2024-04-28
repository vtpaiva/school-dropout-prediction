from graph import Graph, Node, plotGraphPoints, printFinalPath

def recursiveBlindSearch(startPoint, currentNode, timeLimit, finalPaths, pointsVisited):
    for node in currentNode.edgeList.keys():
        if currentNode.getGraphDistance(node) <= timeLimit:
            recursiveBlindSearch(startPoint, Node(node.nodeName, node.xCoord, node.yCoord, 
                                      pastNodes = currentNode.pastNodes + [currentNode], edgeList = node.edgeList), 
                                      timeLimit - currentNode.getGraphDistance(node), finalPaths,
                                      pointsVisited + 1 if node.isTouristic 
                                      and node.nodeName not in [i.nodeName for i in currentNode.pastNodes] else pointsVisited)
            
        if currentNode.nodeName == startPoint.nodeName and currentNode.pastNodes + [currentNode] not in finalPaths:
            finalPaths.append(([i.nodeName for  i in currentNode.pastNodes + [currentNode]], pointsVisited, timeLimit))

def blindSearch(graph, timeLimit):
    recursiveBlindSearch(graph.startingPoint, graph.startingPoint, timeLimit, finalPathsList := [], 0)

    bestPath = max(finalPathsList, key = lambda x: (x[1], x[2]))
    
    return (bestPath[0], bestPath[1], timeLimit - bestPath[2])

a = Node("A", 1, 1)
b = Node("B", 2, 2)
c = Node("C", 3, 3, isTouristic=True)
d = Node("D", 4, 4)
e = Node("E", 5, 5, isTouristic=True)
f = Node("F", 6, 6)
g = Node("G", 7, 7)
h = Node("H", 8, 8, isTouristic=True)
i = Node("I", 9, 9)
j = Node("J", 10, 10, isTouristic=True)
k = Node("K", 11, 11)
l = Node("L", 12, 12, isTouristic=True)

# Adicionando conexões (incluindo pesos arbitrários para exemplificar)
a.addEdges(b)
b.addEdges(c)
c.addEdges(a)  # Ciclo A-B-C-A

a.addEdges(d)
d.addEdges(e)
e.addEdges(a)  # Ciclo A-D-E-A

a.addEdges(f)
f.addEdges(g)
g.addEdges(h)
h.addEdges(a)  # Ciclo A-F-G-H-A

h.addEdges(i)
i.addEdges(j)
j.addEdges(h)  # Ciclo H-I-J-H

j.addEdges(k)
k.addEdges(l)
l.addEdges(j)  # Ciclo J-K-L-J

# Criando o grafo
graph = Graph(a, b, c, d, e, f, g, h, i, j, k, l)

printFinalPath(blindSearch(graph, 25))