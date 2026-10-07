# Lambda -- Parse tree node strategy for printing the special form lambda

from Special import Special

class Lambda(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (lambda params on the first line, body on its own lines.
        Special.printIndented(t, n, p, 2)
