# Regular -- Parse tree node strategy for printing regular lists

from Special import Special

class Regular(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        pass

    def print(self, t, n, p):
        # TODO: Implement this function.
        operator = t.getCar()
        if (n >= 0 and not p and operator.isPair() and
                operator.getCar().isSymbol() and
                operator.getCar().getName() == "lambda" and
                Special.length(operator) >= 2):
            import sys

            sys.stdout.write(' ' * n + '((')
            operator.print(n + 2, True)

            args = t.getCdr()
            while args.isPair():
                sys.stdout.write(' ')
                args.getCar().print(-1)
                args = args.getCdr()
            if not args.isNull():
                sys.stdout.write(' . ')
                args.print(-1)
            sys.stdout.write(')\n')
            return

        Special.printRegular(t, n, p)
