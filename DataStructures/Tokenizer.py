from DataStructures.Stack import Stack
import math

class Tokenizer():
    def __init__(self):
        self.tokens = []

    def tokenize_expression(self, exp):
        """
        Tokenizes the expression and returns a list of tokens
        """
        exp = exp.replace(" ", "")
        tokens = self.raw_tokenize(exp)
        tokens = self.insert_parenthesis(tokens)
        return tokens

    def raw_tokenize(self, exp):
        tokens = []
        current_token = ""
        current_state = ""
        
        for char in exp:
            # In the process of changing states
            if current_state == "number":
                if not char.isnumeric() and char != ".":
                    tokens.append(current_token)
                    current_token = ""
                    current_state = ""
            elif current_state == "variable":
                if not char.isalpha():
                    tokens.append(current_token)
                    current_token = ""
                    current_state = ""
            elif current_state == "operator":
                    if char not in ["+", "-", "*", "/", "**"]:
                        if current_token in ["+", "-", "*", "/", "**"]:
                            tokens.append(current_token)
                            current_token = ""
                            current_state = ""
                        else:
                            raise ValueError(f"Invalid operator: {current_token}")
                    
                    else:
                        if current_token != "*":
                            tokens.append(current_token)
                            current_token = ""
                            current_state = ""
                        else:
                            if char != "*":
                                tokens.append(current_token)
                                current_token = ""
                                current_state = ""

            elif current_state == "function":
                if char not in [*"ln", *"sin", *"cos", *"tan", "["]:
                    tokens.append(current_token)
                    current_token = ""
                    current_state = ""
    
            if char == "(":
                    tokens.append(char)
            elif char in ["+", "-", "*", "/"]:
                # For a negative number, previous token must not be a number or a variable
                if char == "-" and (len(tokens)==0 or not (self.is_operand(tokens[-1]) or tokens[-1].isalpha() or tokens[-1] == ")")):
                    current_token += char
                    current_state = "number"
                else:
                    current_token += char
                    current_state = "operator"
            elif char.isnumeric() or char == ".":
                current_token += char
                current_state = "number"
            elif char.isalpha():
                if current_state == "function":
                    current_token += char
                else:
                    current_token += char
                    current_state = "variable"
            elif char == ")":
                tokens.append(char)

            elif char == "[":
                current_token += char
                current_state = "function"
            
            elif char == "]":
                tokens.append(char)

            elif char == "\\":
                current_token += char
                current_state = "function"

            elif char == " ":
                pass
            
            else:
                raise ValueError(f"Unknown character: {char}")
        
        if current_token != "":
            tokens.append(current_token)
        
        self.set_tokens(tokens)
        return tokens
    
    def insert_parenthesis(self, tokens):
        """
        Inserts parenthesis around the tokens to make the expression more readable
        """
        postfixTokens = self.unorderedInfixToPostfix(tokens)
        infixTokens = self.PostfixToInfix(postfixTokens)

        self.set_tokens(infixTokens)
        return infixTokens
    
    def unorderedInfixToPostfix(self, tokens):
        """
        Convert unordered infix expression to postfix expression using the shunting yard algorithm
        """
        precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '**': 3,
        }

        functions  = {
            '\\ln[': math.log,
            '\\sin[': math.sin,
            '\\cos[': math.cos,
            '\\tan[': math.tan
        }

        PostfixTokens = []
        operator_stack = Stack()

        for token in tokens:
            if self.is_operand(token):
                PostfixTokens.append(token)

            elif token in precedence:
                while not operator_stack.isEmpty() and precedence.get(operator_stack.get(), 0) >= precedence.get(token, 0):
                    PostfixTokens.append(operator_stack.pop())
                operator_stack.push(token)

            elif token in functions:
                operator_stack.push(token)

            elif token == '(':
                operator_stack.push(token)

            elif token == ')':
                while not operator_stack.isEmpty() and operator_stack.get() != '(':
                    PostfixTokens.append(operator_stack.pop())
                if operator_stack and operator_stack.get()== '(':
                    operator_stack.pop()  # Pop the '(' from the stack
            elif token == ']':
                while operator_stack.get() not in functions:
                    PostfixTokens.append(operator_stack.pop())
                function = operator_stack.pop()
                PostfixTokens.append(function)

        # Append any remaining operators from the stack to the PostfixTokens
        while not operator_stack.isEmpty():
            PostfixTokens.append(operator_stack.pop())

        return PostfixTokens
    
    def PostfixToInfix(self, tokens):
        """
        Converts postfix expression to infix expression with proper parentheses
        """
        stack = Stack()
        functions = ['\\ln[', '\\sin[', '\\cos[', '\\tan[']

        for token in tokens:
            if self.is_operand(token):
                stack.push([token])
            elif token in functions:
                operand = stack.pop()
                stack.push(['(', token, *operand, ']', ')'])
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                stack.push(['(', *operand1, token, *operand2, ')'])

        return stack.pop()
    
    def is_operand(self, token):
        return token.isnumeric() or '.' in token or token.isalpha() or ('-' in token and len(token) > 1)


    def get_tokens(self, asExpression=False):
        if asExpression:
            return " ".join(self.tokens)
        return self.tokens
    
    def set_tokens(self, tokens):
        self.tokens = tokens
