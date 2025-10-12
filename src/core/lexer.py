import core.err_disp as err
import core.token_ as tok

import utils.consts as uconst
import utils.gen as ugen
import utils.string as ustr

TT = tok.TokenTypes
lErrs = err.LexerErr


class Lexer:
    def __init__(self) -> None:
        self.src = ""
        self.gotoNxtChr = True
        # TODO: Rm later!
        self.availErrs = ugen.getInnerClses(err.LexerErr, err.Err)

        # Error codes
        self.ERR_UNCLOSED_STR = 1000

    def _nxtChar(self) -> str:
        """
        Read the next character in the source.
        > return: The next character; if the end of the source is reached, then '\0'
        > side-effects: Assigns the next character to self.char and increments self.pos
        """
        if self.char == "\n":
            self.ln += 1
            self.ppos = 0

        self.char = "\0"

        if self.pos < self.lenSrc - 1:
            self.pos += 1
            self.ppos += 1
            self.char = self.src[self.pos]

        return self.char

    def _peekChr(self, n: int = 1) -> str:
        """
        Peek the next n characters in the source.
        > param n: Number of characters to peek
        > return: The next character; if the end of the source is reached, then '\0'
        """
        if self.pos + n < self.lenSrc - 1:
            return self.src[self.pos + n]
        return "\0"

    def _error(self, errCls: type[err.Err], msg: str, token: tok.Token) -> None:
        """
        Throws an error.
        > param errCls: The error class to throw
        > param token: The offending token
        """
        if errCls not in self.availErrs:
            raise err.LogicalErr.NoSuchErr(f"No such lexer error class: '{errCls.__name__}'")
        errCls(msg, token.pos, token.ln, token.ppos)

    def _repInvChr(self, token: tok.Token) -> None:
        """
        Report an invalid character.
        > param token: The offending token
        """
        self._error(lErrs.invChr, f"Invalid character: '{token.val}'", token)

    def _repUnclosedStr(self, token: tok.Token) -> None:
        """
        Report an unclosed string.
        > param token: The offending token
        """
        self._error(lErrs.unclosedStr, f"Unclosed string: '{token.val[1:]}'", token)

    def _chkKeywd(self, txt: str) -> bool:
        """
        Check if the given text is a keyword.
        > param txt: The text to check
        > return: True if the given text is a keyword, otherwise False
        """
        for attr in TT:
            if 900 <= attr.value <= 1199 and attr.name == txt.upper():
                return True
        return False

    def _chkBool(self, txt: str) -> bool:
        """
        Check if the given text is a boolean.
        > param txt: The text to check
        > return: True if the given text is a boolean, otherwise False
        """
        return txt == "true" or txt == "false"

    def _rdNum(self) -> tok.Token:
        """
        Read a number from the source.
        > return: token_.Token object for the read token
        """
        stPos = self.pos
        stLn = self.ln
        stPPos = self.ppos
        dot = False

        while ustr.isDigit(self.char) or self.char == ".":
            if self.char == "." and dot:
                break
            if self.char == ".":
                dot = True
            self._nxtChar()

        endPos = self.pos
        if self.char == "\0":
            endPos = self.pos + 1

        val = self.src[stPos:endPos]

        # Check if the numeric token is immediately followed by another numerical-incompatible
        # token [I can't word it better :(] (like an alphabet or a quote character), which makes
        # numeric literal invalid.
        if endPos < self.lenSrc - 1 and (
            ugen.isAlpha(self.src[endPos]) or self.src[endPos] in uconst.QUOTE_CHRS
        ):

            restOfTheToken = ""
            while not self.src[self.pos].isspace():
                tmp = tok.Token(TT.DUMMY, "", -1, 0, 0)

                if self.src[endPos] in uconst.QUOTE_CHRS:
                    tmp, err = self._rdStr(wQuotes=True)
                    # To compensate for the quote character that's present at the end of the
                    # string if the string had been closed
                    if err != self.ERR_UNCLOSED_STR:
                        self._nxtChar()

                elif ugen.isAlpha(self.src[endPos]):
                    tmp = self._rdIdentOrKeywd()

                restOfTheToken += tmp.val

            return self._newTok(TT.INV, val + restOfTheToken, pos=stPos, ln=stLn, ppos=stPPos)

        if dot:
            return self._newTok(TT.FLOAT, val, pos=stPos, ln=stLn, ppos=stPPos)
        return self._newTok(TT.INT, val, pos=stPos, ln=stLn, ppos=stPPos)

    def _rdStr(self, wQuotes: bool = False) -> tuple[tok.Token, int]:
        """
        Read a string from the source.
        > return: A tuple of token_.Token object for the read token and the integer error code
        """
        stPos = self.pos
        stLn = self.ln
        stPPos = self.ppos
        quote = self.char
        unclosed = False

        self._nxtChar()
        while self.char != quote:
            if self.char == "\n" or self.char == "\0":
                unclosed = True
                break
            self._nxtChar()

        endPos = (self.pos + 1) if unclosed else self.pos
        val = self.src[stPos + 1 : endPos]
        quotes = quote if wQuotes else ""

        if unclosed:
            return (
                self._newTok(TT.INV, quote + val, pos=stPos, ln=stLn, ppos=stPPos),
                self.ERR_UNCLOSED_STR,
            )

        return (
            self._newTok(TT.STR, quotes + val + quotes, pos=stPos, ln=stLn, ppos=stPPos),
            uconst.ERR_SUCCESS,
        )

    def _rdIdentOrKeywd(self) -> tok.Token:
        """
        Read an identifier or a keyword from the source.
        > return: token_.Token object for the read token
        """
        stPos = self.pos
        stLn = self.ln
        stPPos = self.ppos

        while ustr.isAlNum(self.char):
            self._nxtChar()

        endPos = self.pos
        if self.char == "\0":
            endPos = self.pos + 1

        value = self.src[stPos:endPos]
        if self._chkBool(value):
            return self._newTok(TT.BOOL, value, pos=stPos, ln=stLn, ppos=stPPos)
        if self._chkKeywd(value):
            return self._newTok(TT.KEYWD, value, pos=stPos, ln=stLn, ppos=stPPos)
        return self._newTok(TT.IDENT, value, pos=stPos, ln=stLn, ppos=stPPos)

    def _skipWS(self) -> None:
        """
        Skips whitespaces in the source.
        """
        while self.char.isspace():
            self._nxtChar()

    def _skipComments(self) -> None:
        if self.char != "#":
            return
        while self.char != "\n" and self.char != "\0":                                               # type: ignore
            self._nxtChar()
        self._nxtChar()

    def _newTok(
        self,
        type_: TT,
        value: str,
        pos: int | None = None,
        ln: int | None = None,
        ppos: int | None = None,
    ) -> tok.Token:
        """
        Create a new tok.Token object.
        > param type_: The type of the token
        > param value: The value of the token
        > return: token_.Token object created for the data given
        """
        ln = ln if ln is not None else self.ln
        pos = pos if pos is not None else self.pos
        ppos = ppos if ppos is not None else self.ppos
        return tok.Token(type_, value, pos, ln, ppos)

    def _getNxtTok(self) -> tok.Token:
        """
        Get the next token in the source.
        > return: token_.Token object created
        """
        self.gotoNxtChr = True
        self._skipWS()
        # self._skipComments()

        # FOR INCLUDING WHITESPACE IN THE LEXER OUTPUT
        #
        # if self.char == ' ':
        #     token = self._newTok(TT.SPACE, self.char)

        # elif self.char == '\t':
        #     token = self._newTok(TT.TAB, self.char)

        # elif self.char == '\r':
        #     token = self._newTok(TT.CARR_RET, self.char)

        # elif self.char == '\n':
        #     token = self._newTok(TT.NL, self.char)

        if ugen.isAlpha(self.char):
            token = self._rdIdentOrKeywd()
            self.gotoNxtChr = False

        elif ugen.isNum(self.char):
            token = self._rdNum()
            self.gotoNxtChr = False

        elif self.char == ";":
            token = self._newTok(TT.SEMICLN, self.char)

        elif self.char == '"' or self.char == "'":
            token, err = self._rdStr()
            if err == self.ERR_UNCLOSED_STR:
                token = self._newTok(TT.INV, token.val, token.pos, token.ln, token.ppos)
                # self._repUnclosedStr(token)

        elif self.char == "+":
            token = self._newTok(TT.PLUS, self.char)

        elif self.char == "-":
            token = self._newTok(TT.MINUS, self.char)

        elif self.char == "*":
            token = self._newTok(TT.ASTERISK, self.char)

        elif self.char == "/":
            token = self._newTok(TT.FSLASH, self.char)

        elif self.char == "^":
            token = self._newTok(TT.CARET, self.char)

        elif self.char == "$":
            token = self._newTok(TT.DOLLAR, self.char)

        elif self.char == "%":
            token = self._newTok(TT.PERCENT, self.char)

        elif self.char == "(":
            token = self._newTok(TT.LPAREN, self.char)

        elif self.char == ")":
            token = self._newTok(TT.RPAREN, self.char)

        elif self.char == "{":
            token = self._newTok(TT.LFLBRAC, self.char)

        elif self.char == "}":
            token = self._newTok(TT.RFLBRAC, self.char)

        elif self.char == "[":
            token = self._newTok(TT.LSQBRAC, self.char)

        elif self.char == "]":
            token = self._newTok(TT.RSQBRAC, self.char)

        elif self.char == "=":
            if self._peekChr() == "=":
                self._nxtChar()
                token = self._newTok(TT.EQEQ, "==")
            else:
                token = self._newTok(TT.EQ, self.char)

        elif self.char == "!":
            if self._peekChr() == "=":
                self._nxtChar()
                token = self._newTok(TT.NEQ, "!=")
            else:
                token = self._newTok(TT.INV, self.char)
                # self._repInvChr(token)

        elif self.char == "<":
            if self._peekChr() == "=":
                self._nxtChar()
                token = self._newTok(TT.LTEQ, "<=")
            else:
                token = self._newTok(TT.LT, self.char)

        elif self.char == ">":
            if self._peekChr() == "=":
                self._nxtChar()
                token = self._newTok(TT.GTEQ, ">=")
            else:
                token = self._newTok(TT.GT, self.char)

        elif self.char == '#':
            self._skipComments()
            token = self._getNxtTok()

        elif self.char == ",":
            token = self._newTok(TT.COMMA, self.char)

        elif self.char == ".":
            token = self._newTok(TT.DOT, self.char)

        elif self.char == "~":
            token = self._newTok(TT.TILDE, self.char)

        elif self.char == "\0":
            token = self._newTok(TT.EOF, self.char)

        else:
            token = self._newTok(TT.INV, self.char)
            # self._repInvChr(token)

        self._nxtChar() if self.gotoNxtChr else None
        return token

    def tokenise(self, src: str) -> list[tok.Token]:
        allToks: list[tok.Token]

        self.src = src
        self.lenSrc = len(self.src)
        self.char = ""
        self.pos = -1
        self.ln = 1
        self.ppos = 0
        self._nxtChar()

        allToks = []
        allToksApp = allToks.append
        token = self._getNxtTok()

        while token.typ != TT.EOF:
            allToksApp(token)
            token = self._getNxtTok()

        return allToks
