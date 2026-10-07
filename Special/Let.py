# Let -- Parse tree node strategy for printing the special form let

from Special import Special

class Let(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (let on the first line, bindings and body on their own lines.
        Special.printIndented(t, n, p, 1)
