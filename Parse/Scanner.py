# Scanner -- The lexical analyzer for the Scheme printer and interpreter

import sys
import io
from Tokens import *

class Scanner:
    def __init__(self, i):
        self.In = i
        self.buf = []
        self.ch_buf = None

    def read(self):
        if self.ch_buf == None:
            return self.In.read(1)
        else:
            ch = self.ch_buf
            self.ch_buf = None
            return ch
    
    def peek(self):
        if self.ch_buf == None:
            self.ch_buf = self.In.read(1)
            return self.ch_buf
        else:
            return self.ch_buf

    @staticmethod
    def isDigit(ch):
        return ch >= '0' and ch <= '9'

    def getNextToken(self):
        try:
            # It would be more efficient if we'd maintain our own
            # input buffer for a line and read characters out of that
            # buffer, but reading individual characters from the
            # input stream is easier.
            ch = self.read()

            # TODO: Skip white space and comments
            whitespace = " \t\n\r\f"
            initial = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&*/:<=>?^_~"
            subsequent = initial + "0123456789+-.@"
            def scan_identifier(first):
                self.buf = [first.lower()]
                while True:
                    next_ch = self.peek()
                    if next_ch != "" and next_ch in subsequent:
                        self.buf.append(self.read().lower())
                    else:
                        break
                return IdentToken("".join(self.buf))

            while ch != "" and (ch in whitespace or ch == ';'):
                if ch == ';':
                    while ch != "" and ch not in "\n\r":
                        ch = self.read()
                else:
                    ch = self.read()

            # The existing identifier branch below handles uppercase
            # letters. Handle other valid initial characters here.
            if ch != "" and ch in initial and not ('A' <= ch <= 'Z'):
                return scan_identifier(ch)

            if ch in ('+', '-'):
                next_ch = self.peek()
                if next_ch == "" or next_ch in whitespace + '();"':
                    return IdentToken(ch)
                sys.stderr.write("Illegal identifier starting with '" + ch + "'\n")
                return self.getNextToken()
            
            # Return None on EOF
            if ch == "":
                return None
    
            # Special characters
            elif ch == '\'':
                return Token(TokenType.QUOTE)
            elif ch == '(':
                return Token(TokenType.LPAREN)
            elif ch == ')':
                return Token(TokenType.RPAREN)
            elif ch == '.':
                #  We ignore the special identifier `...'.
                return Token(TokenType.DOT)

            # Boolean constants
            elif ch == '#':
                ch = self.read()

                if ch == 't':
                    return Token(TokenType.TRUE)
                elif ch == 'f':
                    return Token(TokenType.FALSE)
                elif ch == "":
                    sys.stderr.write("Unexpected EOF following #\n")
                    return None
                else:
                    sys.stderr.write("Illegal character '" +
                                     chr(ch) + "' following #\n")
                    return self.getNextToken()

            # String constants
            elif ch == '"':
                self.buf = []
                # TODO: scan a string into the buffer variable buf
                while True:
                    ch = self.read()
                    if ch == "":
                        sys.stderr.write("Unexpected EOF in string\n")
                        return None
                    if ch == '"':
                        break
                    if ch == '\\':
                        escaped = self.read()
                        if escaped == "":
                            sys.stderr.write("Unexpected EOF in string\n")
                            return None
                        if escaped not in ('"', '\\'):
                            sys.stderr.write("Illegal string escape\n")
                        self.buf.append(ch)
                        self.buf.append(escaped)
                    else:
                        self.buf.append(ch)
    
                return StrToken("".join(self.buf))

            # Integer constants
            elif self.isDigit(ch):
                i = ord(ch) - ord('0')
                # TODO: scan the number and convert it to an integer
                # make sure that the character following the integer
                # is not removed from the input stream

                while self.isDigit(self.peek()):
                    i = i * 10 + ord(self.read()) - ord('0')
                return IntToken(i)
    
            # Identifiers
            elif ch >= 'A' and ch <= 'Z':
                # or ch is some other vaid first character
                # for an identifier
                self.buf = []
                # TODO: scan an identifier into the buffer variable buf
                # make sure that the character following the identifier
                # is not removed from the input stream
                self.buf.append(ch.lower())
                while True:
                    next_ch = self.peek()
                    if next_ch != "" and next_ch in subsequent:
                        self.buf.append(self.read().lower())
                    else:
                        break
                return IdentToken("".join(self.buf))

            # Illegal character
            else:
                sys.stderr.write("Illegal input character '" + ch + "'\n")
                return self.getNextToken()

        except IOError:
            sys.stderr.write("IOError: error reading input file\n")
            return None


if __name__ == "__main__":
    scanner = Scanner(sys.stdin)
    tok = scanner.getNextToken()
    tt = tok.getType()
    print(tt)
    if tt == TokenType.INT:
        print(tok.getIntVal())
