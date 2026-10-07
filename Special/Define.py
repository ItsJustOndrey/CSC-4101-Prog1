# Define -- Parse tree node strategy for printing the special form define

from Special import Special

class Define(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (define (f args) body...) is printed like lambda;
        # (define x exp) is printed on one line like a regular list.
        rest = t.getCdr()
        if rest.isPair() and rest.getCar().isPair():
            Special.printIndented(t, n, p, 2)
        else:
            Special.printRegular(t, n, p)
