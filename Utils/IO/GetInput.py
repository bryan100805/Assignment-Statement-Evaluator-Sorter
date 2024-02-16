from DataStructures.Tokenizer import Tokenizer
import os

class GetInput:
    # Improved input function with type checking
    def getUserInput(self, question, type = "str", valueRange = None, category = None, value = None, valueList = [], allowQuit = False):
        """
        Gets the user input with type checking

        Parameters
        ----------
        question : str
            The question to be asked with getInput()
        type : str, optional
            The type of input used for type checking, by default "str" 
        valueRange : (list[float] | None), optional
            The valueRange of input to be accepted if type is float or int, by default None
        category : (list[str] | None), optional
            The list of categories to be accepted if type is categorical, by default None
        value : (str | None), optional
            The value to be accepted if type is str, by default None
        valueList : (list[str] | None), optional
            The list of values to be accepted if type is variable, by default None
        """
        
        if type not in ['str', 'categorical', 'int', 'float', 'bool', 'variable', 'equation', 'readEquationFile', 'writeToFile', 'folder', 'matrix', 'matrix_operator', 'strictVariable']:
            raise ValueError(f"Type must be one of the following: 'str', 'categorical', 'int', 'float', 'bool', 'variable', 'equation', 'readEquationFile', 'writeToFile', 'folder', 'matrix', 'matrix_operator', 'strictVariable' but received {type}")

        success = False

        while not success:
            print('\n')
            reply = input(question)

            # If user wants to quit
            if allowQuit and reply.lower() == 'q':
                print("\nQuitting Current Choice...")
                return None

            # Specified int input
            if type == 'int':
                try:
                    reply = int(reply)
                    if valueRange is not None and (reply < valueRange[0] or reply > valueRange[1]):
                        print(f"\nInput must be a number between {valueRange[0]}-{valueRange[1]}")
                    else:
                        success = True
                except ValueError:
                    print("\nInput must be a number")
            
            # Specified string input
            elif type == 'str':
                if (value is None and valueList == []) or reply == value or reply in valueList:
                    success = True

            # Specified float input
            elif type == 'float':
                try:
                    reply = float(reply)
                    if valueRange is not None and (reply < valueRange[0] or reply > valueRange[1]):
                        print(f"\nInput must be a number between {valueRange[0]}-{valueRange[1]}")
                    else:
                        success = True
                except ValueError:
                    print("\nInput must be a float")
        
            # Specified boolean input
            elif type == 'bool':
                if reply.lower() not in ['y', 'n', 'yes', 'no']:
                    print("\nInput must be 'y' or 'n'")

                else:
                    success = True
                    reply = 'y' if reply.lower() in ['y', 'yes'] else 'n'
            
            # Specified categorical input
            elif type == 'categorical':
                # Check upper case
                if reply.upper() not in category:
                    print(f"\nInput must be one of the following: {', '.join(category)}")
            
                else:
                    success = True
                    reply = reply.upper()
            
            # Specified variable input
            elif type == 'variable' or type == 'strictVariable':
                if not reply.isalpha():
                    print("\nInput cannot contain numbers or special characters")

                elif reply not in valueList:
                    if type == 'variable':
                        success = True
                    if type == 'strictVariable':
                        print(f'Variable "{reply}" does not exist')
                        reply = None
                        success = False
                
                else:
                    success = True
            
            # Specified equation input
            elif type == 'equation':
                success, message = self.validateEquation(reply)
                if not success:
                    print(f"\n{message}")
                else:
                    reply = message
                
            # Specified type read from an equation file
            elif type == 'readEquationFile':
                success, message = self.validateReadFile(reply)
                if not success:
                    print(f"\n{message}")
                else:
                    reply = message.split("\n")
                    for index, line in enumerate(reply):
                        # If its an empty line, skip
                        if line == "":
                            continue
                        success, message = self.validateEquation(line)
                        if not success:
                            print(f"\nError on line {index}: {message}")
                            break
                    else:
                        success = True

            # Specified type write to a file
            elif type == 'writeToFile':
                try:
                    with open(reply, "r") as file:
                        overwrite = self.getUserInput(f"File {reply} already exists. Do you want to overwrite it? (y/n)\n", type="bool")
                        if overwrite == 'y':
                            success = True
                except FileNotFoundError:
                    if reply.endswith(".txt"):
                        success = True
                    
                    else:
                        print("\nFile must be a .txt file")
                
                except Exception as e:
                    print(f"An error has occurred: {e}")
            
            # Specified type folder
            elif type == 'folder':
                if os.path.isdir(reply):
                    overwrite = self.getUserInput(f"Folder {reply} already exists. Do you want to overwrite it? (y/n)\n", type="bool")
                    if overwrite == 'y':
                        success = True
                else:
                    success = True

            # Specified type matrix
            elif type == 'matrix':
                success, message = self.validateMatrix(reply)
                if not success:
                    print(f"\n{message}")
                else:
                    reply = message

            # Specified type matrix operator
            elif type == 'matrix_operator':
                success, message = self.validateMatrixOperator(reply)
                if not success:
                    print(f"\n{message}")
                else:
                    reply = message
                
        
        return reply
    
    def validateEquation(self, equation):
        """
        Validates the equation

        Parameters
        ----------
        equation : str
            The equation to be validated

        Returns
        -------
        tuple
            A tuple containing success (bool) and the equation (str) / error message (str)
        """
        success = False
        # Make sure equation can be split into LHS and RHS
        if '=' not in equation:
            message = "Input must contain '='"
            return success, message
        
        equation_list = equation.split('=')
        if len(equation_list) != 2:
            message = "Input must contain only one '='"
            return success, message
            
        LHS, RHS = equation_list[0].strip(), equation_list[1].strip()

        # Make sure LHS is a variable
        if not LHS.isalpha():
            message = "Variables should not contain numbers or special characters"
            return success, message
        
        # Make sure RHS has no special characters
        elif not all([char.isalnum() or char in ['+', '-', '*', '/', '(', ')', ' ', '.', '\\', '[', ']'] for char in RHS]):
            invalid_char = [char for char in RHS if not char.isalnum() and char not in ['+', '-', '*', '/', '(', ')', ' ', '.', '\\', '[']]
            message = f"Expression cannot contain special characters but contains {invalid_char}"
            return success, message
        
        # Make sure RHS contains at least one operator
        elif not any([char in ['+', '-', '*', '/', '**', '\\'] for char in RHS]):
            message = "RHS must contain at least one operator: '+', '-', '*', '/', '**'"
            return success, message
        
        # If RHS contains backslash, make sure it is calling a function
        elif '\\' in RHS:
            # Get all strings between backslashes and '('
            backslash_indices = [i for i, char in enumerate(RHS) if char == '\\']
            open_parantheses_indices = [i for i, char in enumerate(RHS) if char == '[']

            # For two consecutive backslash in backslash_indices, remove the first one
            for i in range(len(backslash_indices)-1):
                if backslash_indices[i+1] - backslash_indices[i] == 1:
                    backslash_indices.pop(i)

            # Match the indices of backslashes with the next closest parantheses
            functions_list = []
            for backslash_index in backslash_indices:
                for parantheses_index in open_parantheses_indices:
                    if parantheses_index > backslash_index:
                        functions_list.append(RHS[backslash_index:parantheses_index])
                        break
            
            if not all([function in ['\\ln', '\\sin', '\\cos', '\\tan'] for function in functions_list]):
                message = "Backslash must be followed by an accepted function: \\ln, \\sin, \\cos, \\tan"
                return success, message


        # Make sure RHS does not contain mismatched parantheses
        circular_parantheses_stack = []
        squared_parantheses_stack = []
        for char in RHS:
            if char == '(':
                circular_parantheses_stack.append(char)
            elif char == ')':
                if len(circular_parantheses_stack) == 0:
                    message = "RHS contains mismatched parantheses"
                    return success, message
                else:
                    circular_parantheses_stack.pop()

            elif char == '[':
                squared_parantheses_stack.append(char)
            elif char == ']':
                if len(squared_parantheses_stack) == 0:
                    message = "RHS contains mismatched squared parantheses"
                    return success, message
                else:
                    squared_parantheses_stack.pop()
        
        if len(circular_parantheses_stack) != 0:
            message = "RHS contains mismatched parantheses"
            return success, message
        
        if len(squared_parantheses_stack) != 0:
            message = "RHS contains mismatched squared parantheses"
            return success, message
        
        # Make sure there are no consecutive operators
        tokens = Tokenizer().raw_tokenize(RHS)

        # Remove all parentheses
        tokens = [token for token in tokens if token not in ['(', ')']]
        
        if tokens[0] in ['+', '-', '*', '/'] or tokens[-1] in ['+', '-', '*', '/']:
            message = "RHS cannot start or end with an operator"
            return success, message
        
        # Ensure there are no consecutive operators other than '**'
        for i in range(len(tokens)-1):
            if tokens[i] in ['+', '-', '*', '/', '**'] and tokens[i+1] in ['+', '*', '/', '**']:
                message = "RHS contains consecutive operators"
                return success, message
            elif tokens[i] in ['\\ln', '\\sin', '\\cos', '\\tan'] and tokens[i+1] in ['+', '-', '*', '/', '**']:
                message = "A function must be followed by an operand"
                return success, message
            
        else:
            success = True
            message = f"{LHS}={RHS}"
            return success, message
        
    def validateReadFile(self, filename):
        """
        Validates the filename

        Parameters
        ----------
        filename : str
            The filename to be validated

        Returns
        -------
        tuple
            A tuple containing success (bool) and the file content (str) / error message (str)
        """
        success = False
        # Check if file extension is .txt
        if not filename.endswith(".txt"):
            message = "File must be a .txt file"
            return success, message

        try:
            with open(filename, "r") as file:
                reply = file.read()
                if reply == "":
                    message = "File is empty"
                    return success, message
                else:
                    success = True
                    return success, reply


        except FileNotFoundError:
            message = f"File {filename} does not exist"
            return success, message

        except Exception as e:
            message = f"An error has occurred while reading the file: {e}"
            return success, message
        
    def validateMatrix(self, matrix):
        '''
        Validates the matrix

        Parameters
        ----------
        matrix : str
            The matrix to be validated
        
        Returns
        -------
        tuple
            A tuple containing success (bool) and the matrix (str) / error message (str)
        '''

        success = False

        # Check if the input is a valid matrix
        if not matrix.startswith("[[") or not matrix.endswith("]]"):
            message = "Matrix input must be surrounded by double square brackets '[[' and ']]'."
            return success, message
                
        # Check if there are values inside the square brackets
        elif matrix[2:-2].strip() == "":
            message = "Matrix input must contain values inside the square brackets."
            return success, message
        
        # Make sure matrix has no special characters
        elif not all([char.isalnum() or char in ['[', ']', ' ', '.', ',', '-'] for char in matrix]):
            invalid_char = [char for char in matrix if not char.isalnum() and char not in ['[', ']', ' ', '.', ',','-']]
            message = f"Expression cannot contain special characters but contains {invalid_char}"
            return success, message
        
        # Make sure RHS does not contain mismatched parantheses
        square_brackets_stack = []
        for char in matrix:
            if char == '[':
                square_brackets_stack.append(char)
            elif char == ']':
                if len(square_brackets_stack) == 0:
                    message = "Matrix contains mismatched square brackets"
                    return success, message
                else:
                    square_brackets_stack.pop()
        
        if len(square_brackets_stack) != 0:
            message = "Matrix contains mismatched square brackets"
            return success, message
                
        # Check if there are commas in between rows by checking presence of comma after 1st closing bracket and every subsequent closing bracket
        if ']' in matrix[2:-2]:
            # Check if there is a comma after every closing bracket
            count_closed_brackets = 0
            for char in matrix[2:-2]:
                if char == ']':
                    count_closed_brackets += 1
                    if matrix[2:-2][matrix[2:-2].index(char)+1] != ',':
                        message = "Every row must be separated by a comma."
                        return success, message

        # Function to check if a string is a number
        def isNumber(s):
            try:
                float(s)
                return True
            except ValueError:
                return False 
        
        # Row validation
        try:
            # Remove white spaces
            matrix_without_spaces = matrix[2:-2].replace(" ", "")
            # Split the matrix into rows
            rows = matrix_without_spaces.split('],[')

            # Split each row into elements
            num_elements_first_row = len(rows[0].split(','))
            # Check if the number of elements in each row is the same
            if not all(len(row.split(',')) == num_elements_first_row for row in rows):
                message = "Number of elements in each row must be the same."
                return success, message
            
            for row in rows:
                # Check if each element in the row is int or float
                if not all(isNumber(element) for element in row.split(',')):
                    message = "Matrix must contain only numbers."
                    return success, message
            
        except Exception as e:
            message = f"An error occurred while parsing the matrix: {e}"
            return success, message
        
        else:
            success = True
            message = f"{matrix}"
            return success, message
        
    def validateMatrixOperator(self, operator):
        '''
        Validates the matrix operator

        Parameters
        ----------
        operator : str
            The operator to be validated
        
        Returns
        -------
        tuple
            A tuple containing success (bool) and the operator (str) / error message (str)
        '''
        success = False

        if operator not in ['+', '-', '*']:
            message = "Matrix operator must be one of the following: '+', '-', '*'."
            return success, message
        
        else:
            success = True
            return success, operator