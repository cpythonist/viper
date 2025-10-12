# Filename: src\\utils\\parse_err_typ_strs.py
# Description: Defines various "error type strings," which are strings used for identifying errors
#              in the program.

"""
This stupidity has been done to ensure that I make no idiotic spelling mistakes. I know this
system of using strings to identify errors in the program is brain-dead, but I started doing it,
and I'm not really looking forward to changing it. And I've made this file so that I can access the
strings from everywhere in the project. Don't really want to handle raw strings at a thousand
places and make the program explode if I make a spelling mistake or make a change.
"""


class ConfigETS:
    cfgStmtMissing = "cfg-cfg-stmt-missing"
    noCfgKeywd = "cfg-no-cfg-keywd"
    invCfgNm = "cfg-inv-cfg-nm"
    invCfgPos = "cfg-inv-cfg-pos"
    noEq = "cfg-no-eq"
    invCfgVal = "cfg-inv-cfg-val"
    noCfgSemcln = "cfg-no-cfg-semcln"


class LetETS:
    noLetKeywd = "let-no-let-keywd"
    noTypKeywd = "let-no-typ-keywd"
    noIdent = "let-no-ident"
    noEq = "let-no-eq"
    exprErr = "let-expr-err"


class IfETS:
    noIf = "if-no-if-keywd"
    exprErr = "if-expr-err"
    bodyErr = "if-body-err"


class GenETS:
    noSemiCln = "gen-no-semicln"
    unexptdCfg = "gen-unexptd-cfg-keywd"
    unexptdTyp = "gen-unexptd-typ-keywd"
    notImpld = "gen-not-impld"


class BreakETS:
    noBreak = "break-no-break-keywd"


class ContiETS:
    noConti = "conti-no-conti-keywd"


class FnETS:
    noFn = "fn-no-fn-keywd"
    exptdTyp = "fn-exptd-typ-keywd"
    noIdent = "fn-no-ident"
    noLParen = "fn-no-lparen"
    noRParen = "fn-no-rparen"
    noParamIdent = "fn-no-param-ident"
    noParamTyp = "fn-no-param-typ"


class WhileETS:
    noWhile = "while-no-while-keywd"
    exprErr = "while-expr-err"
    bodyErr = "while-body-err"


class CmpndStmtETS:
    noLFlBrac = "cmpnd_stmt-no-lflbrac"
    noRFlBrac = "cmpnd_stmt-no-rflbrac"


class ExprETS:
    exptdPrim = "expr-exptd-primary"
    noCloRParen = "expr-no-closing-rparen"


class PrnETS:
    noPrnKeywd = "prn-no-prn-keywd"
    exprErr = "prn-expr-err"


class ChETS:
    noChKeywd = "ch-no-ch-keywd"
    noIdent = "ch-no-ident"
    noEq = "ch-no-eq"
    exprErr = "ch-expr-err"


class RetETS:
    noRetKeywd = "ret-no-ret-keywd"
    exprErr = "ret-expr-err"
