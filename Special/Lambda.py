# Lambda -- Parse tree node strategy for printing the special form lambda

from Special import Special

class Lambda(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        # (lambda params on the first line, body on its own lines.
        if p and n >= 0 and Special.length(t) >= 2:
            import sys

            t.getCar().print(-1)
            t = t.getCdr()
            sys.stdout.write(' ')
            t.getCar().print(-1)
            sys.stdout.write('\n')
            t = t.getCdr()

            while t.isPair():
                t.getCar().print(n + 2)
                t = t.getCdr()
            if not t.isNull():
                sys.stdout.write(' ' * (n + 2) + '. ')
                t.print(-1)
                sys.stdout.write('\n')
            sys.stdout.write(' ' * n + ')\n')
            return

        Special.printIndented(t, n, p, 2)
