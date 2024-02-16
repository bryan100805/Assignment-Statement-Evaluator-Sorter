from DataStructures.Stack import Stack

# Graph
class Graph:
    def __init__(self):
        self.graph = {}

    def addEdge(self, node, neighbour):
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append(neighbour)

    # Check for circular dependency
    def hasCycle(self):
        visited = set()
        stack = Stack()

        for node in self.graph:
            if self.hasCycleHelper(node, visited, stack):
                return True
        return False
    
    def hasCycleHelper(self, node, visited, stack):
        visited.add(node)
        stack.push(node)

        if node in self.graph:
            for neighbour in self.graph[node]:
                if neighbour not in visited:
                    if self.hasCycleHelper(neighbour, visited, stack):
                        return True
                elif neighbour in stack:
                    return True
        stack.pop()
        return False
