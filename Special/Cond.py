# Cond -- Parse tree node strategy for printing the special form cond

from Special import Special

class Cond(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (cond on the first line, each clause on its own line.
        Special.printIndented(t, n, p, 1)
