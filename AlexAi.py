import queue
import pydot
from IPython.display import Image


class Node ():
    def __init__(self, state, operators,adjacents=None,node_coords=None,end_node=None ,operator=None, parent=None, objective=None):
        self.state = state
        self.children = []
        self.operators = operators

        self.operator = operator
        self.parent = parent
        self.objective = objective

        self.adjacents = adjacents
        self.node_coords = node_coords
        self.end_node = end_node

        self.acomulatedCost = 0 if parent is None else parent.acomulatedCost + self.cost()
        self.value = parent.value + '-' + \
            str(operator) if parent is not None else "root"
        self.level = 0 if parent is None else parent.level + 1

    def add_child(self, state, operator):
        node = type(self)(state=state, operator=operator, adjacents=self.adjacents ,parent=self,
                          operators=self.operators, node_coords=self.node_coords, end_node=self.end_node)
        self.children.append(node)
        return node

    def add_node_child(self, node):
        node.level = node.parent.level + 1
        self.children.append(node)
        return node

    def getchildrens(self):
        return [
            self.getState(i)
            if not self.repeatStatePath(self.getState(i))
            else None for i, op in enumerate(self.operators)]

    def getState(self, index):
        pass

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.f() < other.f()

    def repeatStatePath(self, state):
        n = self
        while n is not None and n.state != state:
            n = n.parent
        return n is not None

    def path(self):
        n = self
        result = []
        while n is not None:
            result.append(n)
            n = n.parent
        return result

    def heuristic(self):
        return 0

    def cost(self):
        return 1

    def f(self):
        return self.acomulatedCost+self.heuristic()

    def printPath(self):
        stack = self.path()
        while len(stack) != 0:
            node = stack.pop()
            if node.operator is not None:
                print(
                    f'operador:  {node.operator} \t estado: {node.state}')
            else:
                print(f' {node.state}')


class Tree ():
    def __init__(self, root):
        self.root = root
        self.objective = None

    def reinitRoot(self):
        self.root.operator = None
        self.root.parent = None
        self.root.objective = None
        self.root.children = []
        self.root.level = 0

    def breadthFirst(self, endState):
        self.reinitRoot()
        pq = queue.Queue()
        pq.put(self.root)
        while not pq.empty():
            node = pq.get()
            children = node.getchildrens()
            for i, child in enumerate(children):
                if child is not None:
                    newChild = node.add_child(state=child, operator=i)
                    if endState == child:
                        self.objective = newChild
                        return newChild
                    pq.put(newChild)

    def depthFirst(self, endState):
        self.reinitRoot()
        pq = [self.root]
        while len(pq) != 0:
            node = pq.pop()
            children = node.getchildrens()
            temp = []
            for i, child in enumerate(children):
                if child is not None:
                    newChild = node.add_child(state=child, operator=i)
                    if endState == child:
                        self.objective = newChild
                        return newChild
                    temp.append(newChild)
            pq += reversed(temp)

    def uniformCost(self, endState):
        self.reinitRoot()
        pq = queue.PriorityQueue()
        pq.put((0, self.root))
        while not pq.empty():
            node = pq.get()[1]
            children = node.getchildrens()
            for i, child in enumerate(children):
                if child is not None:
                    newChild = node.add_child(state=child, operator=i)
                    if endState == child:
                        self.objective = newChild
                        return newChild
                    pq.put((newChild.cost(), newChild))

    def bestFirst(self, endState):
        self.reinitRoot()
        pq = queue.PriorityQueue()
        pq.put((0, self.root))
        while not pq.empty():
            node = pq.get()[1]
            children = node.getchildrens()
            for i, child in enumerate(children):
                if child is not None:
                    newChild = node.add_child(state=child, operator=i)
                    if endState == child:
                        self.objective = newChild
                        return newChild
                    pq.put((newChild.heuristic(), newChild))

    def aAsterisk(self, endState):
        self.reinitRoot()
        pq = queue.PriorityQueue()
        pq.put((0, self.root))
        while not pq.empty():
            node = pq.get()[1]
            children = node.getchildrens()
            for i, child in enumerate(children):
                if child is not None:
                    newChild = node.add_child(state=child, operator=i)
                    if endState == child:
                        self.objective = newChild
                        return newChild
                    pq.put((newChild.f(), newChild))
            print(node.level, node.state, node.acomulatedCost, node.heuristic())

    def draw(self):
        graph = pydot.Dot(graph_type='graph')
        nodeGraph = pydot.Node(str(self.root.state)+"-"+str(0),
                               label=str(self.root.state), shape="circle",
                               style="filled", fillcolor="red")
        graph.add_node(nodeGraph)
        self.objective.printPath()
        path = self.objective.path()
        path.pop()
        return Image(self.__drawTreeRec(self.root, nodeGraph, graph, 0, path.pop(), path).create_png())

    def __drawTreeRec(self, node, rootGraph, graph, i, topPath, path):
        if node is not None:
            children = node.children
            for j, child in enumerate(children):
                i = i+1
                color = "white"
                if topPath.value == child.value:
                    if len(path) > 0:
                        topPath = path.pop()
                    color = 'red'
                c = pydot.Node(child.value, label=str(child.state)+r"\n"+r"\n"+"f: "+str(child.f()),
                               shape="circle", style="filled",
                               fillcolor=color)
                graph.add_node(c)
                graph.add_edge(pydot.Edge(rootGraph, c,
                                          label=' o: '+str(child.operator)+'\n c: '+str(child.acomulatedCost)+'\n h: '+str(child.heuristic())))
                graph = self.__drawTreeRec(child, c, graph, i, topPath, path)
            return graph
        else:
            return graph

    def pathStates(self):
        path = self.objective.path()
        return list(reversed([node.state for node in path]))
