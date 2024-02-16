## Binary Tree
class BinaryTree:
    def __init__(self, key, leftTree=None, rightTree=None):
        self.key = key
        self.leftTree = leftTree
        self.rightTree = rightTree

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getLeftTree(self):
        return self.leftTree

    def getRightTree(self):
        return self.rightTree

    def insertLeft(self, key):
        if self.leftTree == None:
            self.leftTree = BinaryTree(key)
        else:
            t = BinaryTree(key)
            self.leftTree, t.leftTree = t, self.leftTree

    def insertRight(self, key):
        if self.rightTree == None:
            self.rightTree = BinaryTree(key)
        else:
            t = BinaryTree(key)
            self.rightTree, t.rightTree = t, self.rightTree

    def printPreorder(self, level=0):
        print(str(level * ".") + str(self.key))
        if self.leftTree != None:
            self.leftTree.printPreorder(level + 1)
        if self.rightTree != None:
            self.rightTree.printPreorder(level + 1)

    def printInOrder(self, level=0):
        if self.leftTree != None:
            self.leftTree.printInOrder(level + 1)
        print(str(level * ".") + str(self.key))
        if self.rightTree != None:
            self.rightTree.printInOrder(level + 1)
    
    def reversePrintInOrder(self, level=0):
        if self.rightTree != None:
            self.rightTree.reversePrintInOrder(level + 1)
        print(str(level * ".") + str(self.key))
        if self.leftTree != None:
            self.leftTree.reversePrintInOrder(level + 1)

    def printPostOrder(self, level=0):
        if self.leftTree != None:
            self.leftTree.printPostOrder(level + 1)
        if self.rightTree != None:
            self.rightTree.printPostOrder(level + 1)
        print(str(level * ".") + str(self.key))

    # Overload the 'in' operator to check if a key is in the tree
    def __contains__(self, key):
        if self.key == key:
            return True
        else:
            if self.leftTree != None:
                if key in self.leftTree:
                    return True
            if self.rightTree != None:
                if key in self.rightTree:
                    return True
        return False
