import sys
import typing as ty

import basicTypes as bt
import err
import other as ot
import tok

ANSI = ot.isANSISupported()
TT = tok.TokenTypes


class Lexer:
    def __init__(self, src:str) -> None:
        "Initialise Lexer object for lexical analysis of the source."
        self.src:str = src + '\0'
        self.char:str = ''
        self.line:int = 1
        self.pos:int = -1
        self.printPos:int = 0

        self.__readChar()
        self.programTyping:int|None = self.__progDecl()
    
    def __progDecl(self):
        self.__skipWhitespaces()
        self.__skipComments()

        if self.char == '~':
            self.__readChar()
        
            while self.char in (' ', '\r', '\t'):
                self.__readChar()
                self.__skipComments()
            
            if self.char not in ('\n', '\0'):
                typing = self.tokenize(progDeclText=True)
                if typing.val not in ("dynamic", "static"):
                    self.__displayError(err.lexErr.illegalProgDeclErr, typing, self.line, self.printPos-typing.size)
                else:
                    while self.char in (' ', '\r', '\t'):
                        self.__readChar()
                    self.__skipComments()
                    
                    if self.char in ('\n', '\0'):
                        self.__readChar()
                        return 1 if typing.val == "dynamic" else 0
                    else:
                        self.__displayError(err.lexErr.illegalProgDeclErr, typing, self.line, self.printPos,
                                            msg=f"Illegal program declaration; expected newline on line {self.line} pos {self.printPos}.")
            else:
                self.__displayError(err.lexErr.illegalProgDeclErr, tok.Token(TT.PLACEHOLDER, bt.VType(), self.line, self.pos, self.printPos, 0), self.line, self.printPos-0,
                                msg=f"Illegal program declaration: Unexpected newline/EOF on line {self.line} pos {self.printPos-0}.")
        
    
    def __checkKeyword(self, ident:str) -> ty.Tuple[bool, TT|str]:
        "Check if the token got in __readIdent() is a keyword."
        for attr in TT:
            if (ident == attr.name.lower()) and (301 <= attr.value <= 400): return True, attr
        return False, ident
    
    def __displayError(self, errType:ty.Type[err.Error], *args:ty.Any, **kwargs:ty.Any) -> None:
        "Display errors."
        sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        sys.stdout.flush()
    
    def __error(self, errType:ty.Type[err.Error], *args:ty.Any, **kwargs:ty.Any) -> None:
        "Display errors."
        # sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        # sys.stdout.flush()
        pass
    
    def __readChar(self) -> None:
        "Read next character in source."
        if self.pos < len(self.src) - 1:
            self.pos += 1
            self.printPos += 1
            self.char = self.src[self.pos]
        else:
            self.char = '\0'
    
    def __peekChar(self):
        "Peeks next character to the current character."
        if self.pos+1 < len(self.src) - 1:
            return self.src[self.pos+1]
        else:
            return '\0'
    
    def __readNum(self):
        "Read number to return the token."
        startPos:int = self.pos
        dotCount:int = 0
        errPrintPos:int = -1

        while ot.isDigit(self.__peekChar()) or self.__peekChar() == '.':
            if self.__peekChar() == '.':
                dotCount += 1
            if dotCount == 2:
                errPrintPos:int = self.printPos
            self.__readChar()
        
        num = self.src[startPos:self.pos+1]
        if dotCount == 0:
            return self.__newToken(TT.INT, bt.VInt(int(num)), self.printPos)
        elif dotCount == 1:
            return self.__newToken(TT.FLOAT, bt.VFloat(float(num)), self.printPos)
        else:
            self.__error(err.lexErr.invalidNum, num, self.line, errPrintPos)
            return self.__newToken(TT.INVALID, bt.VInvalid(num), self.printPos)
    
    def __readSingleQuoteStr(self):
        startPos:int = self.pos

        while self.__peekChar() != '\'':
            if self.__peekChar() in ('\n', '\0'):
                self.__error(err.lexErr.invalidStr, self.src[startPos:self.pos+1], self.line, self.printPos)
                return self.__newToken(TT.INVALID, bt.VInvalid(self.src[startPos+1:self.pos+1]), self.printPos)
            self.__readChar()
        
        self.__readChar()
        return self.__newToken(TT.STRING, bt.VString(self.src[startPos+1:self.pos]), self.printPos)
    
    def __readDoubleQuoteStr(self):
        startPos:int = self.pos

        while self.__peekChar() != '\"':
            if self.__peekChar() in ('\n', '\0'):
                self.__error(err.lexErr.invalidStr, self.src[startPos:self.pos+1], self.line, self.printPos)
                return self.__newToken(TT.INVALID, bt.VInvalid(self.src[startPos+1:self.pos+1]), self.printPos)
            self.__readChar()
        
        self.__readChar()
        return self.__newToken(TT.STRING, bt.VString(self.src[startPos+1:self.pos]), self.printPos)
    
    def __readIdentAndKeyWd(self, returnValForProgDecl:bool=False):
        "Read identifiers and keywords"
        startPos:int = self.pos

        while ot.isAlpha(self.__peekChar()) or ot.isDigit(self.__peekChar()):
            self.__readChar()
        
        if (checkKeywdVal:=self.__checkKeyword(returnVal:=self.src[startPos:self.pos+1]))[0]:
            # if checkKeywdVal[1].name in ("TRUE", "FALSE"):
            #     return self.__newToken(TT.BOOL, bt.VBool(checkKeywdVal[1].name == "TRUE"), self.printPos)
            return self.__newToken(TT.KEYWD, bt.VKeyWd(returnVal), self.printPos) if not returnValForProgDecl else self.__newToken(TT.PROGDECLTEXT, returnVal, self.printPos)
        
        return self.__newToken(TT.IDENT, bt.VIdent(returnVal), self.printPos) if not returnValForProgDecl else self.__newToken(TT.PROGDECLTEXT, returnVal, self.printPos)
    
    def __newToken(self, tokTyp:TT, tokVal:ty.Any, line:int=-1, printPos:int=-1) -> tok.Token:
        "Create a new token, and return created token."
        if line == -1: line = self.line
        if printPos == -1: printPos = self.printPos
        if isinstance(tokVal, str):
            size = len(tokVal)
        else:
            size = tokVal.size()
        return tok.Token(tokTyp, tokVal, line, self.pos, printPos, size)
    
    def __skipWhitespaces(self):
        """
        Ignore whitespace characters (space, carriage return, tab, newline).
        Increase line number if newline is detected and reset the printPos to zero.
        Expand tabs to get actual number of characters.

        Ignore comments (any character after an independent '#' in source till newline).
        """
        while self.char in (' ', '\r', '\t', '\n'):
            if self.char == '\n': self.line += 1; self.printPos = 0
            elif self.char == '\t': self.printPos += (len('\t'.expandtabs()) - 1)
            self.__readChar()

    def __skipComments(self):
        if self.char == '#':
            self.__readChar()
            while self.char not in ('\n', '\0'):
                self.__readChar()
    
    def tokenize(self, progDeclText:bool=False) -> tok.Token:
        "Tokenizes the source. Returns one token at a time."
        self.__skipWhitespaces()
        self.__skipComments()
        
        if self.char in ('+', '-', '*', '/', '^'):
            token = self.__newToken(
                (TT.PLUS,
                 TT.MINUS,
                 TT.ASTERISK,
                 TT.FSLASH,
                 TT.CARET)[('+', '-', '*', '/', '^').index(self.char)],
                bt.VOperator(self.char) # Second argument of __newToken()
            )
        
        elif self.char == '=':
            if self.__peekChar() == '=':
                self.__readChar()
                token = self.__newToken(TT.EQEQ, bt.VOperator('=='))
            else:
                token = self.__newToken(TT.EQ, bt.VAssign('='))
        
        elif self.char == '!':
            if self.__peekChar() == '=':
                self.__readChar()
                token = self.__newToken(TT.NOTEQ, bt.VOperator('!='))
            else:
                self.__error(err.lexErr.invalidChar, self.char, self.line, self.printPos)
                token = self.__newToken(TT.INVALID, bt.VInvalid(self.char))
        
        elif self.char == '<':
            if self.__peekChar() == '=':
                self.__readChar()
                token = self.__newToken(TT.LT, bt.VOperator('<='))
            else:
                token = self.__newToken(TT.LTEQ, bt.VOperator('<'))
        
        elif self.char == '>':
            if self.__peekChar() == '=':
                self.__readChar()
                token = self.__newToken(TT.GT, bt.VOperator('>='))
            else:
                token = self.__newToken(TT.GTEQ, bt.VOperator('>'))
        
        elif self.char == '.':
            if self.__peekChar() not in (' ', '\r', '\t', '\n', '\0'):
                token = self.__newToken(TT.ATTR, bt.VAttribute('.'))
            else:
                token = self.__newToken(TT.INVALID, bt.VInvalid('.'))
        
        elif self.char == ',':
            token = self.__newToken(TT.COMMA, bt.VSeparator(','))
        
        elif ot.isDigit(self.char):
            token = self.__readNum()
        
        elif self.char == '\'':
            token = self.__readSingleQuoteStr()
        
        elif self.char == '\"':
            token = self.__readDoubleQuoteStr()
        
        elif ot.isAlpha(self.char):
            token = self.__readIdentAndKeyWd(returnValForProgDecl=(False if not progDeclText else True))
        
        elif self.char in ('(', ')', '{', '}', '[', ']', ';'):
            token = self.__newToken(
                (TT.LPAREN,
                 TT.RPAREN,
                 TT.LFLOBRAC,
                 TT.RFLOBRAC,
                 TT.LSQBRAC,
                 TT.RSQBRAC,
                 TT.SEMICLN)[('(', ')', '{', '}', '[', ']', ';').index(self.char)],
                bt.VSymbol(self.char) # Second argument of __newToken()
            )
        
        elif self.char == ':':
            token = self.__newToken(TT.COLON, bt.VSymbol(':'))
        
        elif self.char == '~':
            token = self.__newToken(TT.PROGDECL, bt.VProgDecl('~'))
        
        elif self.char in ('\0', ''):
            token = self.__newToken(TT.EOF, bt.VEOF('\0'))
        
        else:
            self.__error(err.lexErr.invalidChar, self.char, self.line, self.printPos)
            token = self.__newToken(TT.INVALID, bt.VInvalid(self.char))
        
        self.__readChar()
        # print(token.val, type(token.val), token.size, self.printPos)
        return token
