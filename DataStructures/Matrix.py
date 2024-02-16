class Matrix:
    def __init__(self, matrix_str):
        self.matrix = self.parseMatrix(matrix_str)

    def parseMatrix(self, matrix_str):
        try:
            rows = eval(matrix_str)
            # Check if the rows are list type
            if not isinstance(rows, list):
                raise ValueError("Invalid matrix format")
            for row in rows:
                # Check if each element in the row is int or float and if the row is list type
                if not isinstance(row, list) or not all(isinstance(element, (int, float)) for element in row):
                    raise ValueError("Invalid matrix format")
                
                # Check if the number of columns in each row is the same
                if len(row) != len(rows[0]):
                    raise ValueError("Invalid matrix format")
                
            return rows
        except Exception as e:
            raise ValueError(f"An error occurred while parsing the matrix: {e}")
            
    def __add__(self, other):
        if isinstance(other, Matrix):
            if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
                raise ValueError("Matrices must have the same dimensions for addition.")
            
            resultMatrix = [[a+b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(self.matrix, other.matrix)]
            return Matrix(str(resultMatrix))
        
        else:
            raise ValueError(f"Unsupported operand type for matrix addition")
        
    def __sub__(self, other):
        if isinstance(other, Matrix):
            if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
                raise ValueError("Matrices must have the same dimensions for subtraction.")
            
            resultMatrix = [[a-b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(self.matrix, other.matrix)]
            return Matrix(str(resultMatrix))
        else:
            raise ValueError(f"Unsupported operand type for matrix subtraction")
        
    def __mul__(self, other):
        if isinstance(other, Matrix):
            if len(self.matrix[0]) != len(other.matrix):
                raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix for multiplication.")
            # Transpose the second matrix to simplify the multiplication process
            resultMatrix = [[sum(a*b for a, b in zip(row_a, col_b)) for col_b in zip(*other.matrix)] for row_a in self.matrix]
            return Matrix(str(resultMatrix))
        elif isinstance(other, (int, float)):
            resultMatrix = [[other * element for element in row] for row in self.matrix]
            return Matrix(str(resultMatrix))
        else:
            raise ValueError(f"Unsupported operand type for matrix multiplication")
        
    def __str__(self):
        return str(self.matrix)