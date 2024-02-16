class Node:
    # Constructor
    def __init__(self):
        self.nextNode = None

# Inherit from Node
class VariableNode(Node):
    def __init__(self, variable, expression, value):
        super().__init__()
        self.variable = variable
        self.expression = expression
        self.value = value
    
    # Check if two nodes are equal
    def __eq__(self, otherNode):
        if otherNode == None:
            return False
        else:
            return self.variable == otherNode.variable and self.value == otherNode.value
    
    # Checks if the node value of the other node is less than the node value of the current node
    def __lt__(self, otherNode):
        if otherNode == None:
            raise TypeError("'<' not supported between instances of 'freqNode' and 'NoneType'")
        
        # First check alphabetically
        if self.variable < otherNode.variable:
            return True
        elif self.variable > otherNode.variable:
            return False
        else:
            # If alphabetically is the same, compare by value
            return (self.value or 0 ) < (otherNode.value or 0)
        
    def __repr__(self):
        return f"VariableNode({self.variable}, {self.expression}, {self.value})"
    
    def __str__(self):
        return f"{self.variable}={self.expression}=> {self.value}"
    
class SortedList:
    def __init__(self):
        self.headNode = None
        self.currentNode = None
        self.length = 0

    def __appendToHead(self, newNode):
        oldHeadNode = self.headNode
        self.headNode = newNode
        self.headNode.nextNode = oldHeadNode
        self.length += 1

    def insert(self, newNode, reverse=False):
        self.length += 1

        # If list is currently empty
        if self.headNode == None:
            self.headNode = newNode
            return
        
        # Check if it is going to be new head
        if not reverse:
            if newNode < self.headNode:
                self.__appendToHead(newNode)
                return
        else:
            if newNode > self.headNode:
                self.__appendToHead(newNode)
                return
        
        # Check it is going to be inserted between any pair of Nodes (left, right)
        leftNode = self.headNode
        rightNode = self.headNode.nextNode

        while rightNode != None:
            if not reverse:
                if newNode < rightNode:
                    leftNode.nextNode = newNode
                    newNode.nextNode = rightNode
                    return
            else:
                if newNode > rightNode:
                    leftNode.nextNode = newNode
                    newNode.nextNode = rightNode
                    return
            leftNode = rightNode
            rightNode = rightNode.nextNode

        # Once we reach here it must be added at the tail
        leftNode.nextNode = newNode
        
    def toList(self):
        listResult = []
        cur = self.headNode
        while cur != None:
            listResult.append(str(cur))
            cur = cur.nextNode
        return listResult


    def __str__(self):
        # We start at the head
        output =""
        node= self.headNode
        firstNode = True
        while node != None:
            if firstNode:
                output = node.__str__()
                firstNode = False
            else:
                output += (',' + node.__str__())
            node= node.nextNode
        return output