# Quote -- Parse tree node strategy for printing the special form quote

import sys
from Special import Special

class Quote(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (quote x), which the parser builds for 'x, is printed as 'x.
        # The quoted expression is printed inline, so quoted special
        # forms come out as regular lists.
        rest = t.getCdr()
        if p or not rest.isPair() or not rest.getCdr().isNull():
            # Not of the form (quote x): print it as written.
            Special.printRegular(t, n, p)
            return
        sys.stdout.write(' ' * n + "'")
        rest.getCar().print(-1)
        if n >= 0:
            sys.stdout.write('\n')
