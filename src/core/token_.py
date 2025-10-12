# token_.py
# Contains token constants and the token object.

import enum


class TokenTypes(enum.Enum):
    # GENERAL
    DUMMY = -3
    INIT = -2
    INV = -1
    EOF = 0
    SEMICLN = 1
    TILDE = 2
    COMMA = 3
    DOT = 4

    KEYWD = 100
    IDENT = 101
    TYP = 102

    # ARITHMETIC OPERATORS
    PLUS = 300
    MINUS = 301
    ASTERISK = 302
    FSLASH = 303
    CARET = 304
    DOLLAR = 305
    PERCENT = 306

    # COMPARISON OPERATORS
    EQEQ = 401
    NEQ = 402
    LT = 403
    GT = 404
    LTEQ = 405
    GTEQ = 406

    # LOGICAL OPERATORS
    NOT = 500
    AND = 501
    OR = 502

    # BRACKETS
    LPAREN = 600
    RPAREN = 601
    LFLBRAC = 602
    RFLBRAC = 603
    LSQBRAC = 604
    RSQBRAC = 605

    # ASSIGNMENT OPERATOR
    EQ = 700

    # KEYWORDS
    # Configuration
    TYPING = 900
    DELIM = 901
    # Types
    INT = 1000
    FLOAT = 1001
    DOUBLE = 1002
    BOOL = 1003
    STR = 1004
    # Others
    TRUE = 1100
    FALSE = 1101
    LET = 1103
    FN = 1104
    RET = 1105
    IF = 1106
    ELIF = 1107
    ELSE = 1108
    WHILE = 1109
    FOR = 1110
    BREAK = 1111
    CONTI = 1112
    LOAD = 1113
    PRN = 1114
    SCN = 1115
    CH = 1116

    # WHITESPACE
    SPACE = 1300
    TAB = 1301
    CARR_RET = 1302
    NL = 1303

    # ERROR-REPORTING TYPES
    PRIMARY = 10000
    UNARY = 10001
    EXPO = 10002
    FACTOR = 10003
    TERM = 10004
    EXPR = 10005

    def __repr__(self) -> str:
        return f"TT.{self.name}"


class Token:
    __slots__ = ("typ", "val", "pos", "ln", "ppos")

    def __init__(self, typ: TokenTypes, val: str, pos: int, ln: int, ppos: int) -> None:
        self.typ = typ
        self.val = val
        self.pos = pos
        self.ln = ln
        self.ppos = ppos

    def __str__(self) -> str:
        return f"Tok[{self.typ.name}: {repr(self.val)}]"
