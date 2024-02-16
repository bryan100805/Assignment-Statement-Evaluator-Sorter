from DataStructures.BinaryTree import BinaryTree
from DataStructures.Stack import Stack
from DataStructures.HashTable import HashTable
from DataStructures.Tokenizer import Tokenizer
import math

tk = Tokenizer()

class ParseTree:
    def __init__(self, exp):
        self.tree = self.build_parse_tree(exp)

    def build_parse_tree(self, exp):
        tokens = tk.tokenize_expression(exp)
        currentTree = BinaryTree("?")
        stack = Stack()
        stack.push(currentTree)
        
        for i, token in enumerate(tokens):
            # RULE 1: If token is '(' add a new node as left child
            # and descend into that node
            if token == "(":
                currentTree.insertLeft("?")
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree()

            # RULE 2: If token is operator set key of current node
            # to that operator and add a new node as right child
            # and descend into that node
            elif token in ["+", "-", "*", "/", "**"]:
                currentTree.setKey(token)
                currentTree.insertRight("?")
                stack.push(currentTree)
                currentTree = currentTree.getRightTree()

            # RULE 3: If token is a float, set key of the current node to that number and return to parent
            elif self.is_numeric(token):
                currentTree.setKey(float(token) if "." in token else int(token))
                parent = stack.pop()
                currentTree = parent

            # RULE 4: If token is ')' go to parent of current node
            elif token == ")":
                if not stack.isEmpty(): 
                    currentTree = stack.pop()

            # RULE 5: If token is a function, create a new node with function as key,
            # add it as the current tree's key, and add a new node as left child.
            elif '\\' in token:
                if not stack.isEmpty():
                    parent = stack.pop()
                    if parent.getKey() == "?":
                        currentTree = parent
                    else:
                        stack.push(parent)

                currentTree.setKey(token)
                currentTree.insertRight(1)
                stack.push(currentTree)
                currentTree = currentTree.getLeftTree()

            # RULE 6: If token is a variable or constant, set the key of the current node to that value.
            elif token.isalpha():
                currentTree.setKey(token)
                parent = stack.pop()
                currentTree = parent

            # End of function
            elif token == "]":
                if not stack.isEmpty():
                    currentTree = stack.pop()

            else:
                raise ValueError(f"Invalid token: {token}")
        
        return currentTree
    
    def evaluate(self, tree, statementsTable=HashTable(100)):
        leftTree = tree.getLeftTree()
        rightTree = tree.getRightTree()
        op = tree.getKey()

        if leftTree is not None and rightTree is not None:

            # If left child is a variable, replace it with the evaluated value
            if leftTree.getKey() in statementsTable.keys:
                secondaryTree = ParseTree(statementsTable[leftTree.getKey()])
                leftValue = secondaryTree.evaluate(secondaryTree.tree, statementsTable=statementsTable)
            # Otherwise if its an unknown variable, return None
            elif leftTree.getKey() not in statementsTable.keys and str(leftTree.getKey()).isalpha():
                leftValue = None
            # Otherwise if its a number, return the number
            else:
                leftValue = self.evaluate(leftTree, statementsTable=statementsTable)

            # If right child is a variable, replace it with the evaluated value
            if rightTree.getKey() in statementsTable.keys:
                secondaryTree = ParseTree(statementsTable[rightTree.getKey()])
                rightValue = secondaryTree.evaluate(secondaryTree.tree, statementsTable=statementsTable)
            # Otherwise if its an unknown variable, return None
            elif rightTree.getKey() not in statementsTable.keys and str(rightTree.getKey()).isalpha():
                rightValue = None
            # Otherwise if its a number, return the number
            else:
                rightValue = self.evaluate(rightTree, statementsTable=statementsTable)

            # If either evaluated value is None, return None
            if leftValue is None or rightValue is None:
                return None

            if op == "+":
                return leftValue + rightValue
            elif op == "-":
                return leftValue - rightValue
            elif op == "*":
                return leftValue * rightValue
            elif op == "/":
                return leftValue / rightValue
            elif op == "**":
                return leftValue ** rightValue
            
            # Functions
            elif op == "\\ln[":
                return math.log(leftValue*rightValue)
            elif op == "\\sin[":
                return math.sin(leftValue*rightValue)
            elif op == "\\cos[":
                return math.cos(leftValue*rightValue)
            elif op == "\\tan[":
                return math.tan(leftValue*rightValue)
            
        else:
            return tree.getKey()
        
    def differentiate(self, tree, variable):
        raw_results = self.differentiate_raw(tree, variable)
        processed_results = ""

        # Format the result
        variable_counter = 0
        for i, char in enumerate(str(raw_results)):
            if char == variable:
                variable_counter += 1
            else:
                if variable_counter > 0:
                    if variable_counter == 1:
                        processed_results += f"{variable}"
                    else:
                        processed_results += f"{variable_counter}*{variable}"
                    variable_counter = 0
                processed_results += char
        
        if variable_counter > 0:
            if variable_counter == 1:
                processed_results += f"{variable}"
            else:
                processed_results += f"{variable_counter}*{variable}"

        processed_results = "".join(Tokenizer().tokenize_expression(processed_results))
        
        return processed_results
        
    def differentiate_raw(self, tree, variable):
        leftTree = tree.getLeftTree()
        rightTree = tree.getRightTree()
        key = tree.getKey()

        # Current node is an operator
        if leftTree is not None and rightTree is not None:
            leftValue = self.evaluate(leftTree)
            rightValue = self.evaluate(rightTree)

            leftDerivative = self.differentiate_raw(leftTree, variable)
            rightDerivative = self.differentiate_raw(rightTree, variable)

            partString = type(leftDerivative) == str or type(rightDerivative) == str or type(leftValue) == str or type(rightValue) == str

            if key == "+":
                if partString:
                    return f"{leftDerivative} + {rightDerivative}"
                
                else:
                    return leftDerivative + rightDerivative
                
            elif key == "-":
                if partString:
                    return f"{leftDerivative} - {rightDerivative}"
                
                else:
                    return leftDerivative - rightDerivative
            
            elif key == "*":

                # If both left and right are expressions containing the variable, use the product rule
                if variable in leftTree and variable in rightTree:
                    if partString:
                        return f"{leftValue}*{rightDerivative} + {rightValue}*{leftDerivative}"
                    else:
                        return leftValue * rightDerivative + rightValue * leftDerivative
                    
                # If left is a constant and right is an expression containing the variable, use the constant rule
                elif variable not in leftTree and variable in rightTree:
                    if partString:
                        return f"{leftValue}*{rightDerivative}"
                    else:
                        return leftValue * rightDerivative
                    
                # If left is an expression containing the variable and right is a constant, use the constant rule
                elif variable in leftTree and variable not in rightTree:
                    if partString:
                        return f"{rightValue}*{leftDerivative}"
                    else:
                        return rightValue * leftDerivative
                    
                # If both left and right are constants, return 0
                else:
                    return 0
                
            elif key == "/":

                # If both left and right are expressions containing the variable, use the quotient rule
                if variable in leftTree and variable in rightTree:
                    if partString:
                        return f"({rightValue}*{leftDerivative} - {leftValue}*{rightDerivative})/({rightValue})**2"
                    
                    else:
                        return (rightValue * leftDerivative - leftValue * rightDerivative) / (rightValue ** 2)
                    
                # If left is a constant and right is an expression containing the variable, use the constant rule
                elif variable not in leftTree and variable in rightTree:
                    if partString:
                        return f"(-{leftValue}*{rightDerivative})/(({rightValue})**2)"
                    else:
                        return (-leftValue * rightDerivative) / (rightValue ** 2)
                    
                # If left is an expression containing the variable and right is a constant, use the constant rule
                elif variable in leftTree and variable not in rightTree:
                    if partString:
                        return f"{leftDerivative}/({rightValue})"
                    else:
                        return leftDerivative / rightValue
                    
                # If both left and right are constants, return 0
                else:
                    return 0
                
            elif key == "**":

                # If both left and right are expressions containing the variable, use the chain rule with u-substitution
                if variable in leftTree and variable in rightTree:
                    return f"{leftValue}**{rightValue} * ({rightDerivative}*\\ln[{leftValue}] + ({rightValue}*{leftDerivative})/{leftValue})"
                    
                # If left is a constant and right is an expression containing the variable, use u-substitution
                elif variable not in leftTree and variable in rightTree:
                    return f"{leftValue}**{rightValue} * {rightDerivative}*\\ln[{leftValue}]"
                
                # If left is an expression containing the variable and right is a constant, use the chain rule
                elif variable in leftTree and variable not in rightTree:
                    if partString:
                        if rightValue == 1:
                            return f"{leftDerivative}"
                        elif rightValue == 2:
                            return f"{rightValue}*{leftValue}"
                        else:
                            return f"{rightValue}*{leftValue}**({rightValue-1})*{leftDerivative}"
                    else:
                        return rightValue * leftValue ** (rightValue - 1) * leftDerivative
                    
                # If both left and right are constants, return 0
                else:
                    return 0
            
            elif key == "\\ln[":
                if partString:
                    return f"{leftDerivative}/{leftValue}"
                else:
                    return leftDerivative / leftValue
                
            elif key == "\\sin[":
                return f"{leftDerivative}*\\cos[{leftValue}]"
                
            elif key == "\\cos[":
                return f"-{leftDerivative}*\\sin[{leftValue}]"
                
            elif key == "\\tan[":
                return f"{leftDerivative}/(\\cos[{leftValue}]**2)"


        # Current node is a constant or variable 
        else:
            if key == variable:
                return 1
            
            elif str(key).isnumeric() or '.' in str(key):
                return 0

    def is_numeric(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False
        
    def drawTree(self):
        return self._draw_node(self.tree, indent="   ")

    def _draw_node(self, node, level=0, indent="   ", left_key_length=0):

        if node is None:
            return (indent[:-4] + str("  " * level) + str((left_key_length-2)*" ") + "/ \\"+ str("_"*(left_key_length-1))+"\n")

        if level == 0:
            indent += (len(str(node.getKey())) -1) * " "

        tree_str = f"{indent+(left_key_length-2)*' '}{node.getKey()} "

        # If the level is less than 1, add a newline and draw the left and right children
        if level < 1:
            if node.getLeftTree() or node.getRightTree():
                tree_str += "\n"
                # Record the length of the left child's key
                left_key_length = len(str(node.getLeftTree().getKey())) if node.getLeftTree() else 0
                tree_str += self._draw_node(None, level + 1, indent[:-7] + "  ", left_key_length)
                tree_str += self._draw_node(node.getLeftTree(), level + 1, indent[:-4] + " ", left_key_length)
                tree_str += self._draw_node(node.getRightTree(), level + 1, indent[:-3] + "  ", left_key_length)
        else:
            # If the node is an operator, draw the left and right children
            if node.getKey() in ["+", "-", "*", "/", "**"]:
                if node.getLeftTree() or node.getRightTree():
                    tree_str += "\n"
                    # Record the length of the left child's key
                    left_key_length = len(str(node.getLeftTree().getKey())) if node.getLeftTree() else 0 
                    
                    pre_indent = -3-level
                    tree_str += self._draw_node(None, level + 1, indent[:-5]+"    ", left_key_length)
                    tree_str += self._draw_node(node.getLeftTree(), level + 1, indent[:pre_indent]+"   "+(level-1)*"  ", left_key_length)
                    tree_str += self._draw_node(node.getRightTree(), level + 1, indent[:-3]+"  ", left_key_length)
        return tree_str