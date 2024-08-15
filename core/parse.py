# TODO:
# 1. Implement dynamic typing system
# 2. Implement for loops
# 3. Done: __expr correct it, return False for True comparisons

import sys
import typing     as ty

import basicTypes as bt
import commons    as comm
import err
import lex
import other      as ot
import tok

# TT is defined here!
TT     = tok.TokenTypes
ANSI   = comm.ANSI
ops    = comm.ops
Int    = bt.VInt
Float  = bt.VFloat
Bool   = bt.VBool
String = bt.VString
inf    = Float(float("inf"))
ninf   = Float(float("-inf"))
nan    = Float(float("nan"))


class Parser:
    def __init__(self, lexer:lex.Lexer) -> None:
        self.lexer                                          = lexer
        self.token                                          = tok.Token(TT.INIT, bt.VType(), -1, -1, -1, 0)
        self.peekToken                                      = tok.Token(TT.INIT, bt.VType(), -1, -1, -1, 0)
        self.tokNum                                         = 0 # aka parPos (for parser position)
        self.symTableOld:dict[str|bt.BaseForAll, ty.Any]    = {}
        self.symTable                                       = comm.Queue()
        self.funcTable:dict[bt.VIdent, dict[bt.VIdent, TT]] = {}
        self.typing                                         = self.lexer.programTyping if self.lexer.programTyping != None \
                                                                                       else 0  # 0 for static, 1 for dynamic
        self.count = 0 # For debugging
        self.err:int|bool = False

        self.__readToken()
        self.__readToken()
    
    def __readToken(self) -> tok.Token:
        if self.token.typ != TT.EOF:
            self.token     =  self.peekToken
            self.peekToken =  self.lexer.tokenize()
            self.tokNum    += 1
        
        return self.token
    
    def __checkToken(self, tokTyp:TT, tokVal:ty.Any=None) -> bool:
        return (self.token.typ == tokTyp) and ((tokVal == None) or (self.token.val == tokVal))
    
    def __matchToken(self, tokTyp:TT, tokVal:bt.BaseForAll|None=None, error:ty.Type[err.Error]|None=None) -> None:
        if self.token.typ == TT.EOF:
            sys.exit(0)
        if (tokTyp == TT.PLACEHOLDER) and (tokVal != None):
            if self.token.val != tokVal:
                self.__error(
                    err.parserErr.syntaxErr if error == None else error,
                    self.token, self.lexer.line, self.lexer.printPos,
                    msg=f"Expected \"{tokVal}\", got \"{self.token.val}\" at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
                )
            else:
                self.__readToken()
        
        elif not self.__checkToken(tokTyp, tokVal):
            self.__error(
                err.parserErr.syntaxErr if error == None else error,
                self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                msg=f"Expected {tokTyp.name}, got \"{self.token.val}\" ({self.token.typ.name}) at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}." \
                    if not (isinstance(self.token.val, bt.VIdent) or self.token.val.val is None) \
                    else f"Expected {tokTyp.name}, got \"{self.token.val.name}\" at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
            )
        
        elif self.__checkToken(tokTyp, tokVal):
            self.__readToken()
        
        else:
            err.fatalErr()
    
    def __error(self, errType:ty.Type[err.Error], *args:ty.Any, readToken:bool=True, **kwargs:ty.Any) -> None:
        "Displays errors."
        sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        sys.stdout.flush()
        self.__readToken() if readToken else None
        self.err = 1
    
    def __checkInfOrNan(self, val:ty.Any) -> bool:
        if ((temp:=isinstance(val, Float)) or (isinstance(val, float))):
            if (temp and ((val == inf) or (val == inf) or (val == nan))) or ((val == float("inf")) or (val == float("-inf")) or (val == float("nan"))):
                return True
        return False
    
    def parse(self):
        print(f"Typing: {"dynamic" if self.typing else "static"}")
        print("PROGRAM-START")
        
        while (not self.__checkToken(TT.EOF)):
            self.__statement()
        
        print("PROGRAM-END")
    
    def __statement(self):
        self.err = 0
        
        if self.__checkToken(TT.KEYWD):
            if self.token.val.val == "print":
                self.err = self.__print()
            
            elif self.token.val.val == "if":
                self.err = self.__if()
            
            elif self.token.val.val == "while":
                self.err = self.__while()
            
            elif self.token.val.val == "for":
                self.err = self.__for()
            
            elif self.token.val.val == "let":
                self.err = self.__let()
            
            elif self.token.val.val == "fun":
                self.err = self.__fun()
            
            else:
                print("Unknown keywd (for now).")
        
        else:
            if isinstance(self.token.val, bt.VIdent):
                self.err = self.__identOthers()   # TODO: fix
            else:
                self.__error(err.parserErr.unexpTok, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                            f"Unexpected token \"{self.token.val if self.token.typ != TT.IDENT else self.token.val.name}\" \
(type {self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
        
        self.__matchToken(TT.SEMICLN)
        while self.token.typ == TT.SEMICLN:
            self.__matchToken(TT.SEMICLN)
    
    def __print(self):
        print("KEYWD: print")
        self.__matchToken(TT.KEYWD, bt.VKeyWd("print"))
        result = self.__expr()
        
        if result is None:
            self.__error(err.parserErr.exprErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, readToken=False)
        
        print(f"VAL: \'{result}\', type: {type(result).__name__}") if not self.err else None
        return self.err
    
    def __if(self):
        # if block
        invIfCondition:bool   = False
        invElifCondition:bool = False

        print("KEYWD: if")
        self.__matchToken(TT.KEYWD, bt.VKeyWd("if"))
        self.__matchToken(TT.LPAREN)

        result = self.__expr()
        if result == None:
            invIfCondition = True

        if not isinstance(result, (Int, Float, Bool, String)):
            self.__error(err.parserErr.exprErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, readToken=False)
        
        self.__matchToken(TT.RPAREN)
        self.__matchToken(TT.LFLOBRAC)

        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        self.__matchToken(TT.RFLOBRAC)

        if not invIfCondition:
            if ot.evaluate(result):
                print("IF-block will be executed!")
            else:
                print("IF-block will NOT be executed!")
        else:
            self.err = 1
        
        # elif block
        elifCount = 0
        while self.__checkToken(TT.KEYWD, "elif"):
            print("KEYWD: elif")
            self.__matchToken(TT.KEYWD, bt.VKeyWd("elif"))
            self.__matchToken(TT.LPAREN)

            result = self.__expr()
            if result == None:
                invElifCondition = True
            
            self.__matchToken(TT.RPAREN)
            self.__matchToken(TT.LFLOBRAC)

            while not self.__checkToken(TT.RFLOBRAC):
                self.__statement()
            
            self.__matchToken(TT.RFLOBRAC)
            elifCount += 1
            
            if not invElifCondition:
                if ot.evaluate(result):
                    print(f"ELIF-block ({elifCount}) will be executed!")
                else:
                    print(f"ELIF-block ({elifCount}) will NOT be executed!")
            else:
                self.err = 1
        
        # else block
        if self.__checkToken(TT.KEYWD, "else"):
            print("KEYWD: else")
            self.__matchToken(TT.KEYWD, bt.VKeyWd("else"))
            self.__matchToken(TT.LFLOBRAC)
            
            while not self.__checkToken(TT.RFLOBRAC):
                self.__statement()
            
            self.__matchToken(TT.RFLOBRAC)
        
        return self.err

    def __while(self):
        invWhileCond:bool = False

        print("KEYWD: while")
        self.__matchToken(TT.KEYWD, bt.VKeyWd("while"))
        self.__matchToken(TT.LPAREN)
        
        result = self.__expr()
        if result == None:
            invWhileCond = True
        
        self.__matchToken(TT.RPAREN)
        self.__matchToken(TT.LFLOBRAC)

        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        
        self.__matchToken(TT.RFLOBRAC)

        if not invWhileCond:
            if ot.evaluate(result):
                print("WHILE-block will be executed!")
            else:
                print("WHILE-block will NOT be executed!")
        else:
            self.err = 1
        
        return self.err

    def __for(self):
        # TODO: Implement for loop
        return self.err

    def __let(self):
        print("KEYWD: let")
        self.__matchToken(TT.KEYWD, bt.VKeyWd("let"))

        if ((str(self.token.val.val).upper() in TT._member_names_) and (TT[str(self.token.val).upper()].value in range(301, 320))):
            typ = self.token.val
            self.__matchToken(TT.KEYWD)
            ident = self.token.val
            self.__matchToken(TT.IDENT)
            self.__matchToken(TT.EQ)
            result = self.__expr()
            
            if result == None:
                self.err = 1
            else:
                if not self.err:
                    self.symTableOld[ident] = result
                    if isinstance(result, getattr(bt, 'V' + typ.val.capitalize())):
                        self.symTable.add([(ident.name, TT[typ.val.upper()], result)])
                    else:
                        self.__error(err.parserErr.typeErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size)
        else:
            self.__error(
                err.parserErr.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                f"Expected identifier type (KEYWD), got type {self.token.typ.name} at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
            )
            if self.__checkToken(TT.IDENT):
                self.__readToken()
                if self.__checkToken(TT.EQ):
                    self.__readToken()
                    result = self.__expr()
                    if result == None:
                        self.__error(err.parserErr.exprErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size)
                else:
                    self.__error(err.parserErr.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                                 f"Expected '=' (EQ), got {self.token.val} ({self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
            else:
                self.__error(err.parserErr.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                             f"Expected IDENT, got {self.token.val} ({self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
        
        return self.err
    
    def __fun(self):
        print("KEYWD: fun")

        funcName:bt.VIdent|None = None
        self.__matchToken(TT.KEYWD, bt.VKeyWd("fun"))
        if isinstance(self.token.val, bt.VIdent):
            funcName = self.token.val
        self.__matchToken(TT.IDENT)
        self.__matchToken(TT.LPAREN)
        parameters = self.__parameters(funcName) if funcName is not None else None
        self.__matchToken(TT.RPAREN)

        if funcName != None and parameters != None:
            self.funcTable[funcName] = parameters # Ignore Pylance error as variable parameters and funcName is checked for None value.

        self.__matchToken(TT.LFLOBRAC)
        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        
        self.__matchToken(TT.RFLOBRAC)
        return self.err
    
    def __identOthers(self):
        print("IDENT: OTHERS")

        if self.token.val.name in self.symTable.zeroes():
            identName = self.token.val.name
            self.__readToken()
            if self.token.typ == TT.EQ:
                print("VALUE OVERWRITE")
                self.__readToken()
                if isinstance(self.token.val, (Int, Float, Bool, String)) and (temp:=self.symTable.get(identName)) and (temp[1] == self.token.typ):
                    # self.symTable[identName] = (self.token.val, self.token.typ)
                    pass
                    
        else:
            self.__error(err.parserErr.unknownIdent, self.token, self.lexer.line, self.lexer.printPos-self.token.size)


    def __expr(self) -> Int|Float|Bool|String|None:
        print("EXPRESSION")

        result  = self.__term()
        invalid = self.__checkInfOrNan(result)

        while (temp:=self.__checkToken(TT.PLUS)) or self.__checkToken(TT.MINUS):
            self.__readToken()
            result2 = self.__term()

            invalid = self.__checkInfOrNan(result2)
            if not invalid and self.__validTypeConcatenation(result, result2):
                try:
                    # Basically checks if either result is an Int, Float or Bool (addition and subtraction possible for them),
                    # or if temp is True (implies the operator is TT.PLUS) and both result and result2 are of type String.
                    if ((isinstance(result, (Int, Float, Bool)) and isinstance(result2, (Int, Float, Bool))) or \
                        (isinstance(result, String) and isinstance(result2, String))):
                        if temp:
                            result += result2
                        else:
                            result -= result2
                    else:
                        invalid = True
                except TypeError:
                    invalid = True
            else:
                invalid = True
        
        if self.isComparisonOp(self.token):
            comp = self.token.val
            self.__readToken()
            result2 = self.__expr()

            invalid = self.__checkInfOrNan(result2)
            if result2 is None:
                invalid = True
            
            if not (invalid or isinstance(result2, String)):
                result = result.__cmp__(result2, comp)
            else:
                invalid = True
        
        if invalid:
            return None
        return result
    
    def __term(self) -> Int|Float|Bool|String:
        result  = self.__unary()
        invalid = self.__checkInfOrNan(result)

        while (temp:=self.__checkToken(TT.ASTERISK)) or self.__checkToken(TT.FSLASH):
            self.__readToken()
            result2 = self.__unary()

            invalid = self.__checkInfOrNan(result2)
            
            if temp and not invalid:
                result *= result2
            if not (temp or invalid):
                if float(result2.val) != 0:
                    result /= result2
                else:
                    self.__error(err.parserErr.zeroDivErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, readToken=False)
        
        if invalid:
            return inf
        return result
    
    def __unary(self) -> Int|Float|Bool|String:
        prevSym:str|ty.Type[bt.VType] = ''

        if (self.__checkToken(TT.MINUS)) or self.__checkToken(TT.PLUS):
            prevSym = str(self.token.val)
            self.__readToken()
        
        result = self.__primary()
        invalid = self.__checkInfOrNan(result)

        if isinstance(result, Int):
            result = Int(int(prevSym + str(result)))
        elif isinstance(result, Float):
            result = Float(float(prevSym + str(result)))
        elif isinstance(result, Bool):
            result = Bool(bool(result))
            result.val = ops[prevSym](result.val) if prevSym else result.val
        else:
            if not prevSym:
                result = String(str(result))
            else:
                self.__error(err.parserErr.typeErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                            msg=f"Illegal operand for unary '{prevSym}': {str(self.token.val)}.")
                invalid = True
        if invalid:
            return inf
        return result
    
    def __primary(self) -> Int|Float|Bool|String|tuple[ty.Any, ty.Any, ty.Any]|None:
        if self.__checkToken(TT.INT) or self.__checkToken(TT.FLOAT):
            result = self.token.val
            self.__readToken()
            return result
        
        elif (temp:=self.__checkToken(TT.KEYWD, bt.VKeyWd("true"))) or self.__checkToken(TT.KEYWD, bt.VKeyWd("false")):
            result = bt.VBool(True) if temp else bt.VBool(False)
            self.__readToken()
            return result
        
        elif self.__checkToken(TT.IDENT):
            if (result:=self.symTable.get(self.token.val.name)) is not None:
                self.__readToken()
                return result
            else:
                self.__error(err.parserErr.unknownIdent, self.token, self.lexer.line, self.lexer.printPos-self.token.size)
                return inf
        
        elif self.__checkToken(TT.LPAREN):
            invalid = False
            self.__readToken()
            result = self.__expr()
            if result == None:
                invalid = True
            self.__matchToken(TT.RPAREN)

            if invalid:
                return inf
            return result
        
        elif self.__checkToken(TT.STRING):
            result = self.token.val
            self.__readToken()
            return result
        
        else:
            return inf

    def __parameters(self, function:bt.VIdent) -> dict[bt.VIdent, TT]|None:
        print("PARAMETERS")
        paras:dict[bt.VIdent, TT] = {}
        
        while (self.token.typ == TT.KEYWD and TT[str(self.token.val).upper()].value in range(301, 340)):
            typ = TT[str(self.token.val).upper()]
            self.__matchToken(TT.KEYWD)
            if isinstance(self.token.val, bt.VIdent):
                paras[self.token.val] = typ
            self.__matchToken(TT.IDENT)
            
            if self.__checkToken(TT.COMMA):
                self.__readToken()
        
        if not self.__checkToken(TT.RPAREN):
            self.__error(err.parserErr.invParamErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, function)
            return None
        
        return paras

    def isComparisonOp(self, token:tok.Token):
        return token.typ in (TT.EQEQ, TT.NOTEQ, TT.LT, TT.LTEQ, TT.GT, TT.GTEQ)

    def __validTypeConcatenation(self, left:ty.Any, right:ty.Any) -> bool:
        return ((isinstance(left, bt.VInt) or isinstance(left, bt.VFloat) or isinstance(left, bt.VBool) or isinstance(left, bt.VString)) \
                and \
                (isinstance(right, bt.VInt) or isinstance(right, bt.VFloat) or isinstance(right, bt.VBool) or isinstance(right, bt.VString)))
