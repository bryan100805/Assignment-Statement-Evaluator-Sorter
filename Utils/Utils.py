from Utils.IO.GetInput import GetInput
from DataStructures.DS import DataStructures
import os

class Utils(GetInput):
        
    def __init__(self): 
        super().__init__() # type: ignore

    # Syntactic sugar for getting user input
    def evaluateKey(self, variable, statementsTable):
        expression = statementsTable[variable]
        parse_tree = DataStructures().ParseTree(expression)
        value = parse_tree.evaluate(parse_tree.tree, statementsTable=statementsTable)
        return expression, value, parse_tree.tree, parse_tree
    
    def detectCircularDependency(self, Graph, statementsTable):
        hasCircularDependency = True
        while hasCircularDependency:
            graph = Graph()
            for key in statementsTable.keys:
                    if key is not None:
                        # Get all the variables in the expression
                        expression = statementsTable[key]
                        tokenized_expression = DataStructures().Tokenizer().tokenize_expression(expression)
                        for token in tokenized_expression:
                            # If token is a variable add an edge to the graph
                            if token.isalpha():
                                graph.addEdge(key, token)
            
            if graph.hasCycle():
                print(f"Circular dependency detected!")
                return True
            return False
        
    def detectDivisionByZero(self, variable, statementsTable):
        hasDivByZero = True
        while hasDivByZero:
            try:
                self.evaluateKey(variable, statementsTable)
                return False
            except ZeroDivisionError:
                print("Cannot divide by zero!")
                return True
    
    # Attempt to create a folder, if it already exists, pass
    def createFolder(self, folderName):
        try:
            os.mkdir(folderName)
        except FileExistsError:
            pass
        return folderName