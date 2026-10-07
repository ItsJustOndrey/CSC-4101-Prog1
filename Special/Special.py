# Special -- Parse tree node strategy for printing special forms

import sys
from abc import ABC, abstractmethod

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.
#
# code that the special forms share into the helpers below.
#
# Each subclass's print(t, n, p) gets the Cons node t to print, the
# indentation n (negative means inline, see Node.py), and p (True if the
# open parenthesis was printed already).  The two helpers below hold the
# printing code shared by all special forms.

class Special(ABC):
    @abstractmethod
    def print(self, t, n, p):
        pass

    # Print t on one line, e.g. (+ 2 3) or (a b . c).  All elements are
    # printed inline, so nested special forms also print as regular lists.
    @staticmethod
    def printRegular(t, n, p):
        if not p:
            sys.stdout.write(' ' * n)
            sys.stdout.write('(')
        first = True
        while t.isPair():
            if not first:
                sys.stdout.write(' ')
            t.getCar().print(-1)
            t = t.getCdr()
            first = False
        if not t.isNull():
            # Improper list: print the final cdr after a dot.
            sys.stdout.write(" . ")
            t.print(-1)
        sys.stdout.write(')')
        if n >= 0:
            sys.stdout.write('\n')

    # Print t with its first k elements on the first line and every
    # remaining element on its own line, indented by 2 more spaces,
    # followed by the closing parenthesis on its own line:
    #   k = 1:  (begin        k = 2:  (if (= n 0)
    #             (set! x 6)            1
    #           )                       2
    #                                 )
    # Falls back to printRegular when printing inline, after an
    # already-printed parenthesis, or when the list is too short.
    @staticmethod
    def printIndented(t, n, p, k):
        if n < 0 or p or Special.length(t) < k:
            Special.printRegular(t, n, p)
            return
        sys.stdout.write(' ' * n)
        sys.stdout.write('(')
        for i in range(k):
            if i > 0:
                sys.stdout.write(' ')
            t.getCar().print(-1)
            t = t.getCdr()
        sys.stdout.write('\n')
        while t.isPair():
            t.getCar().print(n + 2)
            t = t.getCdr()
        if not t.isNull():
            sys.stdout.write(' ' * (n + 2) + ". ")
            t.print(-1)
            sys.stdout.write('\n')
        sys.stdout.write(' ' * n + ")\n")

    # Number of Cons cells in the list t (ignores an improper tail).
    @staticmethod
    def length(t):
        count = 0
        while t.isPair():
            count += 1
            t = t.getCdr()
        return count
