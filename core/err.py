import typing as ty
import tok
if ty.TYPE_CHECKING:
    import basicTypes as bt

TTk = tok.Token
TT = tok.TokenTypes

class Error:
    def __init__(self) -> None:
        self.metatyp:str = "typ"
        self.typ:str = self.__class__.__name__
        self.msg:str = "Base error."
    
    def __str__(self) -> str:
        return f"{self.metatyp}.{self.typ}: {self.msg}"


class lexErr:
    def __init__(self) -> None:
        self.metatyp:str = "lexErr"
        self.msg:str = "Base lexer error."

    class invalidChar(Error):
        def __init__(self, char:str, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "lexer"
            self.msg:str = f"Invalid char \'{char}\' at line {line} pos {pos}." if msg == None else msg

    class invalidNum(Error):
        def __init__(self, num:str, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "lexer"
            self.msg:str = f"Invalid number \"{num}\" at line {line} pos {pos}." if msg == None else msg

    class invalidStr(Error):
        def __init__(self, string:str, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "lexer"
            self.msg:str = f"Invalid string \"{string}\" at line {line} pos {pos}." if msg == None else msg
    
    class illegalProgDeclErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "viper"
            self.msg:str = f"Illegal program declaration at token \"{token.val}\" (type {token.typ.name}) on line {line} pos {pos}." if msg == None else msg


class parserErr:
    class invalidToken(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Invalid token \"{token.val}\" (type {token.typ}) at line {line} pos {pos}." if msg == None else msg


    class assignTypMismatch(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Cannot assign value of type \"{token.val}\" to type \"{token.typ}\" at line {line} pos {pos}." if msg == None else msg


    class illegalOp(Error):
        def __init__(self, op:str, line:int=-1, pos:int=-1, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Unsupported operation \"{op}\" at line {line} pos {pos}." if msg == None else msg


    class invalidType(Error):
        def __init__(self, typ:str, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Invalid type \"{typ}\" at line {line} pos {pos}." if msg == None else msg


    class invalidStatement(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Invalid statement at token \"{token.val}\" (type {token.typ}) at line {line} pos {pos}." if msg == None else msg


    class unknownIdent(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Unknown identifier \"{token.val.name}\" at line {line} pos {pos}." if msg == None else msg


    class syntaxErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Syntax error at token \"{token.val}\" (type {token.typ.name}) on line {line} pos {pos}." if msg == None else msg


    class exprErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Invalid expression at line {line} pos {pos}." if msg == None else msg


    class conditionErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Invalid condition at line {line} pos {pos}." if msg == None else msg


    class invParamErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, function:"bt.VIdent", msg:str|None=None) -> None:
            super().__init__()
            self.metatyp = "parser"
            self.msg = (f"Invalid parameter at token \"{token.val.val}\" (type {token.typ.name}) for function \"{function.name}\" on line {line} pos {pos}." \
                            if token.val.val is not None else \
                            f"Invalid parameter at token \"{token.val.name}\" (type {token.typ.name}) for function \"{function.name}\" on line {line} pos {pos}.") if msg == None else msg
    
    
    class zeroDivErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp = "parser"
            self.msg = f"Division by zero at token \"{token.val}\" (type {token.typ.name}) at line {line} pos {pos}."


    class typeErr(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Type mismatch for left and right operand at token \"{token.val}\" ({token.typ.name}) line {line} pos {pos}." if msg == None else msg


    class unexpTok(Error):
        def __init__(self, token:TTk, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str = "parser"
            self.msg:str = f"Unexpected token \"{token.val}\" (type {token.typ.name}) at line {line} pos {pos}." if msg == None else msg


class viperErr:
    class zeroDivErr(Error):
        def __init__(self, token:tok.Token, line:int, pos:int, msg:str|None=None) -> None:
            super().__init__()
            self.metatyp:str =  "viper"
            self.msg:str     = f"Division by zero at token {token.val.val} (type {token.typ.name}) on line {line} pos {pos}." if not msg else msg


class fatalErr:
    def __init__(self) -> None:
        print("A fatal error has occured in Viper. Please raise an issue on the project's GitHub Issues page.")
