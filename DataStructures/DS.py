from DataStructures.Stack import Stack
from DataStructures.SortedList import Node, VariableNode, SortedList
from DataStructures.HashTable import HashTable
from DataStructures.BinaryTree import BinaryTree
from DataStructures.ParseTree import ParseTree
from DataStructures.Graph import Graph
from DataStructures.Matrix import Matrix
from DataStructures.Tokenizer import Tokenizer

class DataStructures():
    # Accessors
    def Stack(self):
        return Stack()
    
    def HashTable(self, size):
        return HashTable(size)
    
    def BinaryTree(self, key, leftTree=None, rightTree=None):
        return BinaryTree(key, leftTree, rightTree)
    
    def ParseTree(self, exp):
        return ParseTree(exp)
    
    def Node(self):
        return Node()
    
    def VariableNode(self, variable, expression, value):
        return VariableNode(variable, expression, value)
    
    def SortedList(self):
        return SortedList()
    
    def Graph(self):
        return Graph()
    
    def Tokenizer(self):
        return Tokenizer()
    
    def Matrix(self, matrix_str):
        return Matrix(matrix_str=matrix_str)
    


    
