import numpy as np, math, copy
import matplotlib.pyplot as plt
    
# Classe grafo com ponto inicial, arestas, nós e pontos turísticos
class Graph:
    def __init__(self, *args) -> None:
        self.startingPoint = args[0]
        self.edges = {i.nodeName:i.edgeList for i in args}
        self.nodes, self.touristicPoints = args, [i for i in args if i.isTouristic]
    
# Classe nó com nome, coordenadas e variáveis para o algoritmo A*
class Node:
    def __init__(self, nodeName, xCoord, yCoord, timeSpent = 0, isTouristic =  False, edgeList = None, pastNodes = None) -> None:
        self.nodeName = nodeName
        self.xCoord, self.yCoord = xCoord, yCoord
        self.timeSpent = timeSpent
        self.isTouristic = isTouristic
        self.isVisited = False
        self.pastNodes = pastNodes if pastNodes != None else []
        self.edgeList = edgeList if edgeList != None else {}
        self.realPath = {}
        
    def __repr__(self) -> str:
        return f"\"{self.nodeName}\" at ({self.xCoord}, {self.yCoord})"
    
    def addEdges(self, *args):
        self.edgeList.update({i[0] if isinstance(i, tuple) else 
                              i: i[1] if isinstance(i, tuple) else 1 for i in args})
        
    def getEuclideanDistance(self, other) -> float:
        return math.sqrt((self.xCoord - other.xCoord)**2 + (self.yCoord - other.yCoord)**2)
    
    def getGraphDistance(self, other) -> float:
        if self is other:
            return 0
        
        return self.edgeList.get(other, np.inf)

#   Heurística de distância euclidiana
def euclideanHeuristic(originNode, destinyNode):
    return originNode.getEuclideanDistance(destinyNode)   

#Algoriitmo do A*
def shortestPath(graph, heuristic, originNode, destinyNode):
    if originNode == destinyNode:
        return originNode, 0
    
    openNodes, closedNodes = [], set()

    currentNode = (Node(originNode.nodeName, originNode.xCoord, originNode.yCoord), 0, heuristic(originNode, destinyNode))
    
    openNodes.append(currentNode)
    
    while openNodes:
        closedNodes.add(currentNode[0].nodeName)
        
        if currentNode[0].nodeName == destinyNode.nodeName:
            return currentNode[0].pastNodes + [currentNode[0]], currentNode[1]
        
        currentNeighbors = graph.edges[currentNode[0].nodeName]
        
        openNodes.extend([(Node(i.nodeName, i.xCoord, i.yCoord, pastNodes = currentNode[0].pastNodes + [currentNode[0]], timeSpent = j + currentNode[0].timeSpent), 
        j + currentNode[0].timeSpent, heuristic(i, destinyNode)) for i, j in currentNeighbors.items() if i.nodeName not in closedNodes])
        
        tmpNode = min(openNodes, key = lambda x:(x[1] + x[2]))
        
        if currentNode in openNodes:
            openNodes.remove(currentNode)

        currentNode = tmpNode
        
    return None, np.inf

#Redução do Grafo a apenas pontos turísticos
def reduceGraph(originalGraph):
    touristicPointsCopy = copy.deepcopy([originalGraph.startingPoint] + originalGraph.touristicPoints)
    
    for i in touristicPointsCopy:
        shortestPathList = {node : shortPath for node in touristicPointsCopy if i != node and 
                            (shortPath := shortestPath(originalGraph, euclideanHeuristic, i, node))[1] != np.inf}
        
        i.edgeList = {a:  b[1] for a, b in shortestPathList.items()}
        i.realPath = {a : b[0][1:] for a, b in shortestPathList.items()}
                
    return Graph(*touristicPointsCopy)

# Função para encontrar melhor rota
def maxPointsPath(reducedGraph, timeLimit):
    startPoint = reducedGraph.startingPoint
    
    finalPath, currentNode = [startPoint.nodeName], startPoint
    timeSpent = pointsVisited = 0
        
    while (avaiable := [(i, j) for i, j in currentNode.edgeList.items() if not i.isVisited and i != startPoint
                        and j + timeSpent + i.getGraphDistance(startPoint) <= timeLimit]):
        
        currentEdge = min(avaiable, key = lambda x: x[1])
        
        timeSpent += currentEdge[1]
        
        finalPath.extend(i.nodeName for i in currentNode.realPath.get(currentEdge[0]))
        
        currentNode = currentEdge[0]
        
        currentNode.isVisited = True
        
        pointsVisited += 1
        
    return finalPath + [i.nodeName for i  in currentNode.realPath.get(startPoint)], pointsVisited, timeSpent + currentNode.getGraphDistance(startPoint)

def printFinalPath(bestPath):
    print(" -> ".join(bestPath[0]), f"| Pontos visistados: {bestPath[1]} | Custo: {bestPath[2]}")

def plotGraphPoints(graph):
    for point in graph.nodes:
        for edgePoint in point.edgeList:
            plt.annotate('', xy=(edgePoint.xCoord, edgePoint.yCoord), xytext=(point.xCoord, point.yCoord),
            arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='simple', linewidth=0.0))
            
        if point == graph.startingPoint:
            plt.plot(point.xCoord, point.yCoord, 'g^')
        else:
            plt.plot(point.xCoord, point.yCoord, 'r*' if point.isTouristic else 'ko')
            
    plt.show()

if __name__ == "__main__":        
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
    reduced_graph = reduceGraph(graph)

    result = maxPointsPath(reduced_graph, 180)
    
    printFinalPath(result)