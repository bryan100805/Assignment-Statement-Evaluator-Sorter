from DataStructures.DS import DataStructures
from Algorithms.Algo import Algorithms
from Utils.Utils import Utils

import networkx as nx
import matplotlib.pyplot as plt

data_structures = DataStructures()
algo = Algorithms()
utils = Utils()

class MenuOptions():
    """
    This class contains the methods that are used by the CipherCLI class
    Each method is a menu option that the user can choose from
    """
    def __init__(self):
        super().__init__()
        self.options = {
            '1': self.addModifier,
            '2': self.displayAssignments,
            '3': self.evaluateVariable,
            '4': self.readAssignmentFromFile,
            '5': self.sortAssignment,
            '6': self.visualiseTree,
            '7': self.evaluateMatrix,
            '8': self.differentiateVariable,
            '9': self.assignmentAnalysis,
            '10': self.Exit
        }
        self.statementsTable = data_structures.HashTable(size=256)
        self.isRunning = True

    # Option 1
    def addModifier(self):
        equation = utils.getUserInput("Enter the assignment statement you want to add/modify:\nFor example, a=(1+2)\nOtherwise, press 'q' to quit\n", type="equation", allowQuit=True)
        if equation is None: return
        variable, expression = equation.split("=")
        # Tokenize the expression
        tk = data_structures.Tokenizer()
        tk.tokenize_expression(expression)
        expression = tk.get_tokens(asExpression=True)
        self.statementsTable[variable] = expression

        # Ensure no circular dependency
        while utils.detectCircularDependency(data_structures.Graph, self.statementsTable) or utils.detectDivisionByZero(variable, self.statementsTable):

            # Delete the variable from the hash table
            del self.statementsTable[variable]
            # Get user input again
            equation = utils.getUserInput("Enter the assignment statement you want to add/modify:\nFor example, a=(1+2)\nOtherwise, press 'q' to quit\n", type="equation", allowQuit=True)
            if equation is None: 
                return
            variable, expression = equation.split("=")
            # Tokenize the expression
            tk = data_structures.Tokenizer()
            tk.tokenize_expression(expression)
            expression = tk.get_tokens(asExpression=True)
            self.statementsTable[variable] = expression
    
    # Option 2
    def displayAssignments(self):
        variables_tuple = [tuple([variable]) for variable in self.statementsTable.keys if variable is not None]
        if len(variables_tuple) == 0:
            print("NO ASSIGNMENT FOUND")
            return
        
        # Sort the variables alphabetically using merge sort
        print(f"\nCURRENT ASSIGNMENTS:\n{'*'*20}")
        sorted_variables = algo.MergeSort(variables_tuple, 1, [1])
        for variable, *_ in sorted_variables:
            expression, value, *_ = utils.evaluateKey(variable, self.statementsTable)
            print(f"{variable}={expression}=> {value}")
        
    # Option 3
    def evaluateVariable(self):
        variable = utils.getUserInput("Please enter the variable you want to evaluate:\n", type="strictVariable", valueList=self.statementsTable.keys)

        if variable is not None:
            print("Expression Tree:\n")
            _, value, tree, _ = utils.evaluateKey(variable, self.statementsTable)
            tree.reversePrintInOrder()
            print(f'\nValue for variable "{variable}" is {value}')
        
    # Option 4
    def readAssignmentFromFile(self):
        lines = utils.getUserInput("Please enter input file: ", type="readEquationFile")
        for line in lines:
            line = line.strip()
            if line: # If line is not empty
                variable, expression = line.split("=")[0].strip(), line.split("=")[1].strip()
                # Tokenize the expression
                tk = data_structures.Tokenizer()
                tk.tokenize_expression(expression)
                expression = tk.get_tokens(asExpression=True)
                self.statementsTable[variable] = expression

                # Ensure no circular dependency
                while utils.detectCircularDependency(data_structures.Graph, self.statementsTable) or utils.detectDivisionByZero(variable, self.statementsTable):
                    print("Error Detected in the input file. Exiting Option...")
                    # Delete the variable from the hash table
                    del self.statementsTable[variable]
                    return

        # Display current assignments after reading from the file
        self.displayAssignments()
        

    # Option 5
    def sortAssignment(self):
        variables = [variable for variable in self.statementsTable.keys if variable is not None]
        if len(variables) == 0:
            print("NO ASSIGNMENT FOUND")
            return
        
        # Create a list of tuples, where each tuple contains the value, variable and length of the variable
        unsorted_assignments = []
        for variable in variables:
            expression, value, *_  = utils.evaluateKey(variable, self.statementsTable)
            unsorted_assignments.append((value if value is not None else float("-inf"), variable, len(variable)))
        
        # Sort the assignments based on evaluated value in descending order, followed by alpabetical order
        sorted_assignments = algo.MergeSort(unsorted_assignments, 3, [0, 1, 1])
        
        output_file_path = utils.getUserInput("Please enter output file: ", type="writeToFile")
        prev_value = "start"
        with open(output_file_path, "w") as output_file:
            for _, variable, _ in sorted_assignments:
                expression, value, *_ = utils.evaluateKey(variable, self.statementsTable)

                if prev_value == "start":
                    output_file.write(f"*** Statements with value=> {value}\n")

                elif value != prev_value:
                    output_file.write(f"\n*** Statements with value=> {value}\n")
                    
                prev_value = value
                output_file.write(f"{variable}={expression}\n")

    # Option 6
    def visualiseTree(self):

        variable = utils.getUserInput("Please enter the variable you want to evaluate:\n", type="strictVariable", valueList=self.statementsTable.keys)

        if variable is not None:
            print("Expression Tree:\n")
            *_, parse_tree = utils.evaluateKey(variable, self.statementsTable)

            print(f"Visualisation of the parse tree for variable {variable}:\n")
            print(parse_tree.drawTree())

    # Option 7
    def evaluateMatrix(self):
        while True:
            try:
                matrix_str1 = utils.getUserInput(f"Enter the first matrix in the list format (e.g., [[1,2,3],[4,5,6],[7,8,9]]):\n", type="matrix")
                matrix_str2 = utils.getUserInput(f"Enter the second matrix in the list format:\n", type="matrix")

                matrix1 = DataStructures().Matrix(matrix_str1)
                matrix2 = DataStructures().Matrix(matrix_str2)

                matrix_operator = utils.getUserInput(f"Enter the matrix operator (e.g., +, -, *):\n", type="matrix_operator")

                if matrix_operator == "+":
                    result_matrix = matrix1 + matrix2
                elif matrix_operator == "-":
                    result_matrix = matrix1 - matrix2
                elif matrix_operator == "*":
                    result_matrix = matrix1 * matrix2
                else:
                    raise ValueError(f"Unsupported matrix operator: {matrix_operator}")
                
                print(f"\n Result: \n {result_matrix}")
                break
            except Exception as e:
                print(f"\nMatrix Operation is Unsuccessful: {e}")
                print("\nPlease try again.")

    # Option 8
    def differentiateVariable(self):
        variable_to_be_differentiated = utils.getUserInput("Please enter the variable you want to differentiate:\n", type="strictVariable", valueList=self.statementsTable.keys)
        variable = utils.getUserInput("Please enter the variable with respect to which you want to differentiate:\n", type="variable", valueList=self.statementsTable.keys)

        # Retrieve the expression and check if it contains any variables that have the evaluated value of None
        expression = self.statementsTable[variable_to_be_differentiated]
        tk = data_structures.Tokenizer()
        tk.tokenize_expression(expression)
        tokens = tk.get_tokens(asExpression=False)

        for index, token in enumerate(tokens):
            if token != variable and token.isalpha():
                if token not in self.statementsTable.keys:
                    print(f"Cannot differentiate expression with variable {token} not found in memory")
                    print("Exiting Option...")
                    return
                _, value, *_ = utils.evaluateKey(token, self.statementsTable)
                if value is None:
                    print(f"Cannot differentiate expression with variable {token} having value of None")
                    print("Exiting Option...")
                    return
                
                else:
                    tokens[index] = str(value)

        # Join the tokens to form the expression
        simplified_expression = "".join(tokens)

        # Differentiate the expression
        parse_tree = DataStructures().ParseTree(simplified_expression)
        derivative = parse_tree.differentiate(parse_tree.tree, variable)
        parse_tree = DataStructures().ParseTree(derivative)
        value = parse_tree.evaluate(parse_tree.tree, statementsTable=self.statementsTable)
        print(f"\nDerivative of {variable_to_be_differentiated} with respect to {variable} is {derivative}=>{value}")

        choice = utils.getUserInput("Do you want to add this derivative to the memory? (y/n): ", type="bool")
        if choice=='y':
            derivate_name = utils.getUserInput("Please enter the name for the derivative: ", type="variable")
            self.statementsTable[derivate_name] = derivative
            print(f"\nDerivative {derivate_name}={derivative} has been added to memory")

    # Option 9
    def assignmentAnalysis(self):
        folder = utils.getUserInput("Please enter the folder to save the assignment analysis graph: ", type="folder")
        # Create folder if it does not exist
        utils.createFolder(folder)

        # Get every variable and its dependencies
        variables = [variable for variable in self.statementsTable.keys if variable is not None]

        # Create a directed graph
        g = nx.DiGraph()
        referenced = set()

        variable_references_counter = DataStructures().HashTable(size=256)
        references = []

        for variable in variables:
            expression = self.statementsTable[variable]
            tokenized_expression = DataStructures().Tokenizer().tokenize_expression(expression)
            for token in tokenized_expression:
                # If token is a variable add an edge to the graph
                if token.isalpha():
                    # Add to already referenced variables
                    referenced.add(variable)
                    referenced.add(token)

                    # Count number of times referenced
                    if variable_references_counter[token] is None:
                        variable_references_counter[token] = 1
                    else:
                        variable_references_counter[token] += 1

                    # Add edge to the graph
                    references.append((variable, token))
                    g.add_edge(variable, token)
            
        # Add the nodes that are not referenced
        for variable in variables:
            if variable not in referenced:
                g.add_node(variable)

        # Draw the graph
        pos = nx.shell_layout(g)
        # Add the labels outside the nodes
        nx.draw(g, pos, with_labels=True, node_size=2000, node_color="skyblue", node_shape="s", font_size=10, font_color="black", font_weight="bold", edge_color="black", linewidths=1, width=2, alpha=0.7)
        plt.title("Assignment Analysis")
        # Save the graph to a file
        plt.savefig(f"{folder}/assignment_analysis_graph.png", dpi=500, bbox_inches="tight")

        # Draw a bar chart of the number of references for each variable
        plt.figure()
        # Sort the variables based on the number of references
        sorted_variables = algo.MergeSort([(variable_references_counter[variable], variable) for variable in variable_references_counter.keys if variable is not None], 2, [0, 1])
        reference_counts, variables = zip(*sorted_variables)
        plt.bar(variables, reference_counts)
        plt.xlabel("Variables")
        plt.ylabel("Number of times Referenced")
        plt.title("Number of times Referenced for each Variable")
        plt.xticks(rotation=90)
        plt.savefig(f"{folder}/assignment_analysis_bar_chart.png", dpi=500, bbox_inches="tight")

        # Get all variables from references
        all_variables = list(set([variable for reference in references for variable in reference]))
        all_tokens = list(set([token for reference in references for token in reference]))

        # Create a matrix of references to store the references
        matrix = [[0 for _ in range(len(all_variables))] for _ in range(len(all_tokens))]
        # Set -1 for same variable
        for i in range(len(all_variables)):
            matrix[i][i] = -1

        # Add 1 each time a reference is found for a variable
        for reference in references:
            for token in reference:
                matrix[all_tokens.index(reference[0])][all_variables.index(reference[1])] += 1

        # Plot a heatmap of the references
        plt.figure()
        plt.imshow(matrix, cmap='viridis', interpolation='nearest')
        plt.colorbar()
        plt.title("References Heatmap")
        plt.xticks(range(len(all_variables)), all_variables, rotation=90)
        plt.yticks(range(len(all_tokens)), all_tokens)
        plt.savefig(f"{folder}/assignment_analysis_heatmap.png", dpi=500, bbox_inches="tight")

        print(f"\nPlots have been saved in the folder {folder}")

    # Option 10
    def Exit(self):
        self.isRunning = False
        print("\nBye, thanks for using ST1507 DSAA: Assignment Statement Evaluator & Sorter")

    # Synthetic sugar for evaluating a key
    def evaluateKey(self, variable):
        expression = self.statementsTable[variable]
        parse_tree = data_structures.ParseTree(expression)
        value = parse_tree.evaluate(parse_tree.tree, statementsTable=self.statementsTable)
        return expression, value, parse_tree.tree, parse_tree