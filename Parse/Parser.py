# Parser -- the parser for the Scheme printer and interpreter
#
# Defines
#
#   class Parser
#
# Parses the language
#
#   exp  ->  ( rest
#         |  #f
#         |  #t
#         |  ' exp
#         |  integer_constant
#         |  string_constant
#         |  identifier
#    rest -> )
#         |  exp+ [. exp] )
#
# and builds a parse tree.  Lists of the form (rest) are further
# `parsed' into regular lists and special forms in the constructor
# for the parse tree node class Cons.  See Cons.parseList() for
# more information.
#
# The parser is implemented as an LL(0) recursive descent parser.
# I.e., parseExp() expects that the first token of an exp has not
# been read yet.  If parseRest() reads the first token of an exp
# before calling parseExp(), that token must be put back so that
# it can be re-read by parseExp() or an alternative version of
# parseExp() must be called.
#
# If EOF is reached (i.e., if the scanner returns None instead of a token),
# the parser returns None instead of a tree.  In case of a parse error, the
# parser discards the offending token (which probably was a DOT
# or an RPAREN) and attempts to continue parsing with the next token.

import sys
from Tokens import TokenType

class Parser:
    def __init__(self, s):
        self.scanner = s

    def parseExp(self):
        # TODO: write code for parsing an exp

        from Tree import BoolLit, Cons, Ident, IntLit, Nil, StrLit

        tok = self._nextToken()
        if tok is None:
            return None

        tt = tok.getType()

        if tt == TokenType.LPAREN:
            return self.parseRest()
        if tt == TokenType.FALSE:
            return BoolLit.getInstance(False)
        if tt == TokenType.TRUE:
            return BoolLit.getInstance(True)
        if tt == TokenType.INT:
            return IntLit(tok.getIntVal())
        if tt == TokenType.STR:
            return StrLit(tok.getStrVal())
        if tt == TokenType.IDENT:
            return Ident(tok.getName())
        if tt == TokenType.QUOTE:
            quoted = self.parseExp()
            if quoted is None:
                self.__error("expected an expression after quote")
            return None
        return Cons(Ident("quote"), Cons(quoted, Nil.getInstance()))

    def parseRest(self):
        # TODO: write code for parsing a rest
        from Tree import Cons, Nil

        items = []

        while True:
            tok = self._nextToken()
            if tok is None:
                self.__error("unexpected EOF in list")
                return None

            tt = tok.getType()

            if tt == TokenType.RPAREN:
                tail = Nil.getInstance()
                break

            if tt == TokenType.DOT:
                if not items:
                    self.__error("dot must follow an expression")
                    continue

                next_tok = self._nextToken()
                if next_tok is None or next_tok.getType() == TokenType.RPAREN:
                    self.__error("expected an expression after dot")
                    return None

                self._putBack(next_tok)
                tail = self.parseExp()
                if tail is None:
                    return None

                closing = self._nextToken()
                if closing is None or closing.getType() != TokenType.RPAREN:
                    self.__error("expected ')' after dotted expression")
                    return None
                break

            self._putBack(tok)
            item = self.parseExp()
            if item is None:
                return None
            items.append(item)

        for item in reversed(items):
            tail = Cons(item, tail)
        return tail
        return None


    # TODO: Add any additional methods you might need

    def _nextToken(self):
        if hasattr(self, "_saved_token"):
            tok = self._saved_token
            del self._saved_token
            return tok
        return self.scanner.getNextToken()

    def _putBack(self, tok):
        if hasattr(self, "_saved_token"):
            raise RuntimeError("parser lookahead is already occupied")
        self._saved_token = tok

    def __error(self, msg):
        sys.stderr.write("Parse error: " + msg + "\n")
