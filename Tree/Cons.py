# Cons -- Parse tree node class for representing a Cons node

from Tree import Node
from Tree import Ident
from Special import *

class Cons(Node):
    def __init__(self, a, d):
        self.car = a
        self.cdr = d
        self.parseList()

    # parseList() `parses' special forms, constructs an appropriate
    # object of a subclass of Special, and stores a pointer to that
    # object in variable form.  It would be possible to fully parse
    # special forms at this point.  Since this causes complications
    # when using (incorrect) programs as data, it is easiest to let
    # parseList only look at the car for selecting the appropriate
    # object from the Special hierarchy and to leave the rest of
    # parsing up to the interpreter.
    def parseList(self):
        # TODO: implement this function and any helper functions
        # you might need
        if self.car.isSymbol():
            name = self.car.getName()
            if name == "quote":
                self.form = Quote()
            elif name == "lambda":
                self.form = Lambda()
            elif name == "begin":
                self.form = Begin()
            elif name == "if":
                self.form = If()
            elif name == "let":
                self.form = Let()
            elif name == "cond":
                self.form = Cond()
            elif name == "define":
                self.form = Define()
            elif name == "set!":
                self.form = Set()
            else:
                self.form = Regular()
        else:
            self.form = Regular()

    def isPair(self):
        return True

    def getCar(self):
        return self.car

    def getCdr(self):
        return self.cdr

    # Changing the car can change which special form this is.
    def setCar(self, a):
        self.car = a
        self.parseList()

    def setCdr(self, d):
        self.cdr = d

    def print(self, n, p=False):
        self.form.print(self, n, p)

if __name__ == "__main__":
    c = Cons(Ident("Hello"), Ident("World"))
    c.print(0)
