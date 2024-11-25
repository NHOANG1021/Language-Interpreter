class Statement:
    """
    A base class to handle all basic statement functionality
    """
    def __init__(self, statement: list, info: list):
        """
        Initializes with the statement in a list and the
        info as a list of tuples
        """
        self.statement = statement
        self.info = info

class VarValue(Statement):
    """
    Derived class of Statement to handle statements containing
    variables and/or values
    """
    def __init__(self, statement: list, info: list, var = None, value = None):
        """
        Initializes with the same values as Statement, alongside
        var and value being initialized to None for each object
        """
        super().__init__(statement, info)
        self.var = var
        self.value = value

    def let(self, variables: dict):
        """
        Assigns var and value when called.
        """
        self.var = self.statement[1]
        self.value = self.statement[2]


    def print(self):
        """
        Assigns value when called.
        """
        self.value = self.statement[1]

    # Unable to test due to input()
    def innum(self, user_input):
        """
        Assigns var when called, value when user enters input.
        """
        self.var = self.statement[1]
        self.value = user_input

    # Unable to test due to input()
    def instr(self, user_input):
        """
        Assigns var when called, value when user enters input.
        """
        self.var = self.statement[1]
        self.value = user_input

    def add(self):
        """
        Assigns var and val when called.
        """
        self.var = self.statement[1]
        self.value = self.statement[2]

    def sub(self):
        """
        Assigns var and val when called.
        """
        self.var = self.statement[1]
        self.value = self.statement[2]

    def mult(self):
        """
        Assigns var and val when called.
        """
        self.var = self.statement[1]
        self.value = self.statement[2]

    def div(self):
        """
        Assigns var and val when called.
        """
        self.var = self.statement[1]
        self.value = self.statement[2]

class Goto(Statement):
    """
    Class to handle GOTO statements
    """
    def __init__(self, statement: list, info: list):
        super().__init__(statement, info)
        self.target = statement[-1]

# Unable to test due to exit()
    def check_target(self, labels: dict, total: int, current: int, variables: dict):
        """
        Using the info mentioned in the function definition, checks if
        the target is a valid one
        """
        # print(self.target)
        # print(labels)
        if type(self.target) is int:
            if self.target == 0:
                print('Can not jump to 0')
                exit()
            elif self.target + current > total:
                print('Can not jump outside of total lines')
                exit()
            elif self.target + current <= 0:
                print('Can not jump to a negative line')
                exit()
        elif self.target in variables.keys():
            pass
        elif self.target not in labels.keys():
            print('Can not jump to unknown label')
            exit()

        # print('CHECKED')


class GotoIf(Goto):
    """
    Derived class of Goto, handles GOTO statements if they have
    a conditional that needs to be checked.
    """
    def __init__(self, statement: list, info: list, conditional = None):
        super().__init__(statement, info)
        self.target = statement[1]
        self.conditional = conditional

    def get_conditional(self):
        self.conditional = self.info[4][2]

    def check_conditional(self, left: int, right: int) -> bool:
        """
        Checks the conditional and returns True or False
        """

        if self.conditional == '<':
            return left < right
        elif self.conditional == '<=':
            return left <= right
        elif self.conditional == '>':
            return left > right
        elif self.conditional == '>=':
            return left >= right
        elif self.conditional == '=':
            return left == right
        elif self.conditional == '<>':
            return left != right

    def replace_conditional(self, variables: dict) -> tuple:
        """
        Makes sure that the left and right operands are both int
        before returning the value to be used in a conditional
        """
        left = self.statement[3]
        right = self.statement[5]

        if type(left) is not int:
            if left in variables.keys():
                left = variables[left]

        if type(right) is not int:
            if right in variables.keys():
                right = variables[right]

        return left, right