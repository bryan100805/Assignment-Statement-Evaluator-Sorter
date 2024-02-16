# README
This project involves the implementation of an application in Python that can evaluate assignment statements with fully parenthesized mathematical expressions, employing parse trees as an underlying mechanism. 
The primary objective is to provide users with a versatile tool that facilitates the manipulation, evaluation and organization of mathematical expressions involving variables, while coding in the OOP framework, making use of different types of synthetic sugar 
(i.e. Operator Overloading, Function Overloading, Inheritance, Encapsulation). 
In the process of adding, modifying and sorting the assignment statements, several data structures like Graphs, Hashmaps, Stack and Linked List, as well as advanced algorithms like Merge Sort, Shunting Yard, Depth First Search and InOrder Traversal has been used.

#### Option 1 - Adding/Modifying Assignment Statements
Upon selecting Option ‘1’, the users will be prompted to enter assignment statements with fully parenthesized mathematical expressions as per the requirements. 
The option has also been enhanced to be able to accept assignment statements without parenthesis as well support the use of negative numbers. 
These statements will be stored for future use via hashmaps, and users can continue to add more assignment statements.
Advanced error handling is also included such as for checking circular dependency and checking for division by zero when adding assignments.

#### Option 2 - Displaying Current Assignment Statements
Option ‘2’ allows users to evaluate and print the parse tree for all currently loaded assignment statements. This display will include the value of variables, ensuring users can track the results of their entered expressions.

#### Option 3 - Evaluating a Single Variable
Option ‘3’ is dedicated to evaluating and printing the parse tree of an individual variable. Users will be guided on how to specify the variable for evaluation, and the resulting parse tree will be displayed in an in-order traversal format.

#### Option 4 - Read Assignment Statements from File
Option ‘4’ prompts users to enter an input text file that contains multiple assignment statements. 
Subsequently, these statements are evaluated, and the outcomes are presented in an organized fashion within the output. 
The display adheres to ascending alphabetical order, followed by ascending length based on the variable name, facilitated by merge sort.

#### Option 5 - Sort Assignment Statements
Option ‘5’ enables users to sort loaded assignment statements via merge sort of the evaluated values of the assignment statements in descending order. 
In the scenario where the evaluated values are equal, precedence is given to the variable name sorted in ascending alphabetical order, followed by the length of the variable names in ascending order. 
The sorted results will be written to an output file prompted to the users.

#### Option 6 - Visualize the parse tree of an expression
Option '6' enables users to visualise the parse tree in the GUI based on the inorder traversal from the variable the user key in as input, which the application would refer back to the hashmap to return the tree for the visualisation.

#### Option 7 - Evaluate Matrix Operation
Option '7' enables users to evaluate matrices by asking users to input 2 matrices. 
Making use of operator overloading, the application ensures the matrices are evaluated based on the overwritten matrix logic which ensures basic operations like addition, subtraction and multiplication can be done to the matrices. 
At the same time, the application validates errors like ensuring the matrices are conformable for multiplication and ensure that matrices are same dimensions for addition and subtractions.
It also keep track of mismatched brackets, ensure commas are within the elements and many more..
