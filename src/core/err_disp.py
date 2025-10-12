import inspect as ip

from utils import string as ustr
from utils import consts as uconst


class Err:
    """
    Base class for all Viper errors.
    """

    typ = "base"

    def __init__(self, msg: str, pos: int, ln: int, prnPos: int) -> None:
        self.parentNm = ip.getmro(self.__class__)[1].__name__
        self.nm = self.__class__.__name__
        self.msg = msg
        self.pos = pos
        self.ln = ln
        self.prnPos = prnPos
        print(
            ustr.vRepr(
                "{}E:{} [L{} P{}] {}.{}: {}".format(
                    uconst.ANSI_BOLD_RED,
                    uconst.ANSI_RESET,
                    self.ln,
                    self.prnPos,
                    self.typ,
                    self.nm,
                    msg,
                )
            )
        )


class LogicalErr:
    class NoSuchErr(Exception):
        pass

    class ArrElemTypErr(Exception):
        pass

    class NotImplementedErr(Exception):
        pass

    class InvPeekVal(Exception):
        pass

    class ExptdDiffTyp(Exception):
        pass

    class InvTyp(Exception):
        pass

    class NoSuchErrTypStr(Exception):
        pass

    class ChkTokNoData(Exception):
        pass

    class InvArg(Exception):
        pass


class LexerErr:
    class invChr(Err):
        typ = "lexer"

    class invNum(Err):
        typ = "lexer"

    class unclosedStr(Err):
        typ = "lexer"


class ParserErr:
    class invTok(Err):
        typ = "parser"

    class unexpTok(Err):
        typ = "parser"

    class invPrim(Err):
        typ = "parser"

    class invConfigVal(Err):
        typ = "parser"


class SemanticErr:
    class undefdVar(Err):
        typ = "semantics"

    class typMismatch(Err):
        typ = "semantics"

    class invOp(Err):
        typ = "semantics"
