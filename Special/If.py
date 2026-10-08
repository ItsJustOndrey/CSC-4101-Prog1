# If -- Parse tree node strategy for printing the special form if

from Special import Special

class If(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (if test on the first line, each branch on its own line.
        Special.printIndented(t, n, p, 2)
