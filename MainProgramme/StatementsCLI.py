from MainProgramme.MenuOptions import MenuOptions
from Utils.Utils import Utils

utils = Utils()

class StatementsCLI(MenuOptions):
    """
    This class handles the user interface of the program.
    It inherits from the MenuOptions class, which contains the methods
    """
    def __init__(self):
        super().__init__()

    def starting_screen(self):
        starting_text=f"{'*'*59}\n* ST1507 DSAA: Evaluating & Sorting Assignment Statements *\n*{'-'*57}*"
        starting_text += f"\n*{' '*57}*"
        starting_text += f"\n* - Done by: Bryan Tan (2214449) & Ryan Yeo (2214452){' '*5}*\n* - Class DAAA/FT/2B/01{' '*35}*"
        starting_text += f"\n*{' '*57}*"
        starting_text += f"\n{'*'*59}"
        print(starting_text)
        
    def continueProgram(self):
        utils.getUserInput("Press Enter key, to continue....", value="")
    

    def getMenuInput(self):
        menu_text = """
Please select your choice: ('1','2','3','4','5','6','7','8','9','10')
    1. Add/Modify assignment statement
    2. Display current assignment statements
    3. Evaluate a single variable
    4. Read assignment statements from file
    5. Sort assignment statements
    6. Visualize the parse tree of an expression
    7. Evaluate matrix operations
    8. Differentiate an expression
    9. Assignment Statistics
    10. Exit
Enter choice:  """

        menu_input = utils.getUserInput(menu_text, "int", [1,10])
        return menu_input

    def run(self):
        self.starting_screen()
        while self.isRunning:
            self.continueProgram()
            menu_input = self.getMenuInput()
            self.options[str(menu_input)]()
