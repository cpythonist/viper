import dataclasses as dcs
import typing as ty

import core.ast_nodes as ast
import core.lexer as lex
import core.err_disp as err
import core.token_ as tok

import utils.consts as uconst
import utils.gen as ugen
import utils.parse_utils as upar

import core.parser.parse_break as parbr
import core.parser.parse_conti as parcon
import core.parser.parse_cfg as parcfg
import core.parser.parse_ch as parch
import core.parser.parse_cmpnd_stmt as parcmpndstmt
import core.parser.parse_expr as parexpr
import core.parser.parse_fn as parfn
import core.parser.parse_if as parif
import core.parser.parse_let as parlet
import core.parser.parse_prn as parprn
import core.parser.parse_ret as parret
import core.parser.parse_stmt as parstmt
import core.parser.parse_while as parwhile

TT = tok.TokenTypes
allNodeTyps = (
    ast.CfgNode
    | ast.LetNode
    | ast.ChNode
    | ast.IfNode
    | ast.WhileNode
    | ast.BreakNode
    | ast.ContiNode
    | ast.PrnNode
    | ast.FnNode
    | ast.StmtNode
    | ast.NotImplementedNode
    | ast.ErrNode
)


@dcs.dataclass
class LangConfig:
    typing: str
    delim: str


class Parser(
    parcfg.CfgParserMixin,
    parexpr.ExprParserMixin,
    parstmt.StmtParserMixin,
    parcmpndstmt.CmpndStmtParserMixin,
    parlet.LetParserMixin,
    parif.IfParserMixin,
    parwhile.WhileParserMixin,
    parbr.BreakParserMixin,
    parcon.ContiParserMixin,
    parfn.FnParserMixin,
    parprn.PrnParserMixin,
    parch.ChParserMixin,
    parret.RetParserMixin,
):
    def __init__(self, src: str, lexer: lex.Lexer) -> None:
        self.tree: list[ast.ASTNode]

        self.lexer = lexer
        self.allToks = self.lexer.tokenise(src)
        self.lenAllToks = len(self.allToks)
        self.token = tok.Token(TT.INIT, "", -1, 0, 0)
        self.tokenIdx = -1
        self.availErrs = ugen.getInnerClses(err.ParserErr, err.Err)
        self.tree = []
        self.parseErrs = upar.ParseErrs()
        self.treeApp = self.tree.append
        self.parseErrsAdd = self.parseErrs.add

        self.primValidTyps = (TT.INT, TT.FLOAT, TT.BOOL, TT.STR)
        self.unaryOps = (TT.PLUS, TT.MINUS)
        self.factorOps = (TT.ASTERISK, TT.FSLASH, TT.DOLLAR, TT.PERCENT)
        self.termOps = (TT.PLUS, TT.MINUS)
        self.exprOps = (TT.EQEQ, TT.NEQ, TT.LT, TT.LTEQ, TT.GT, TT.GTEQ)
        self.resyncTyps = (TT.SEMICLN, TT.LFLBRAC, TT.EOF)
        self.wsToks = (TT.SPACE, TT.TAB, TT.CARR_RET, TT.NL)
        self.resyncKeywds = (
            "let",
            "if",
            "elif",
            "else",
            "while",
            "for",
            "break",
            "conti",
        )
        self.semiClnErr = False

        self.EOF_TOK = tok.Token(TT.EOF, "\0", self.lexer.pos, self.lexer.ln, self.lexer.ppos)
        self.ERR_MATCH_TOK_ERR = 2000
        self.ERR_UNEXP_TOK = 2001

        self.nxtTok()

    def nxtTok(self) -> tok.Token:
        """
        Get the next token from the lexer.
        > return: The current token after advancing one token.
        """
        self.tokenIdx += 1
        if self.tokenIdx > self.lenAllToks - 1:
            self.token = self.EOF_TOK
        else:
            self.token = self.allToks[self.tokenIdx]
        return self.token

    def chkTok(
        self, typ: TT | None = None, val: ty.Any = None, token: tok.Token | None = None
    ) -> bool:
        token = self.token if token is None else token

        if typ is not None and val is None:
            return token.typ == typ

        elif typ is not None and val is not None:
            return token.typ == typ and token.val == val

        elif typ is None and val is not None:
            return token.val == val

        else:
            raise err.LogicalErr.ChkTokNoData("No data given in function parser.Parser.chkTok(...)")

    def chkTokRange(
        self, span: list[int] | tuple[int, int], tokenOrTT: tok.Token | TT | None = None
    ):
        """
        Check if a token's value in the enum class token_.TokenTypes is in the specified range.
        > param span: The range to check (both inclusive)
        > param tokenOrTT: The token to check
        > return: True if the token type's value lies in the range specified, False otherwise
        """
        tokenOrTT = self.token if tokenOrTT is None else tokenOrTT
        if type(tokenOrTT) == tok.Token:
            reqdVal = tokenOrTT.typ.value
        elif type(tokenOrTT) == TT:
            reqdVal = tokenOrTT.value
        else:
            raise err.LogicalErr.InvArg(
                f"Invalid argument for param 'tokenOrTT' in {__file__}.Parser.chkTokRange(...)"
            )

        # Check if your dumbass made some stupid mistake
        isSpanListOrTuple = isinstance(span, (list, tuple))  # type: ignore
        areSpanElemsInt = isinstance(span[0], int) and isinstance(span[1], int)  # type: ignore
        if len(span) != 2 or not (isSpanListOrTuple and areSpanElemsInt):
            raise err.LogicalErr.InvArg(
                f"Invalid argument for param 'span' in {__file__}.Parser.chkTokRange(...)"
            )

        if reqdVal in range(span[0], span[1] + 1):
            return True
        return False

    def peekTok(self, n: int = 1) -> tok.Token:
        """
        Peek n tokens forwards.
        > param n: Number of tokens to peek
        > return: The peeked token
        """
        # TODO: Rm in final build if needed
        if n < 1:
            raise err.LogicalErr.InvPeekVal(
                f"Invalid peek value in function parser.Parser.peekTok(...): '{n}'"
            )
        if self.tokenIdx + n > self.lenAllToks - 1:
            return self.EOF_TOK
        return self.allToks[self.tokenIdx + n]

    def isTokPresentInPeek(self, typ: TT | None = None, val: ty.Any = None) -> bool:
        n = 1
        while True:
            nPeek = self.peekTok(n)
            typCond = nPeek.typ == typ if typ is not None else True
            valCond = nPeek.val == val if val is not None else True
            if typCond and valCond:
                return True
            elif nPeek.typ == TT.EOF:
                return False
            n += 1

    def skipWSToks(self, exclude: ty.Iterable[TT] = []) -> None:
        while self.token.typ in self.wsToks and self.token.typ not in exclude:
            self.nxtTok()

    def skipTillResyncToks(self, typ: TT | list[TT] = TT.DUMMY, val: ty.Any = None) -> None:
        """
        Skip tokens in the source till a resynchronisation token is hit.
        """
        if typ == TT.DUMMY and val is None:
            while self.token.typ not in self.resyncTyps:
                if self.token.typ == TT.KEYWD and self.token.val in self.resyncKeywds:
                    break
                self.nxtTok()

        elif val is None:
            typCond = lambda: self.token.typ != typ
            # If a list of types are given
            if isinstance(typ, (list, tuple)):
                typCond = lambda: self.token.typ not in typ

            while typCond():
                if self.token.typ == TT.EOF:
                    break
                self.nxtTok()

        elif typ == TT.DUMMY:
            valCond = lambda: self.token.val != val
            # If a list of values are given
            if isinstance(val, (list, tuple)):
                valCond = lambda: self.token.val not in val

            while valCond():
                if self.token.typ == TT.EOF:
                    break
                self.nxtTok()

        else:
            typCond = lambda: self.token.typ != typ
            valCond = lambda: self.token.val != val
            # If a list of types are given
            if isinstance(typ, (list, tuple)):
                typCond = lambda: self.token.typ not in typ
            # If a list of values are given
            if isinstance(val, (list, tuple)):
                valCond = lambda: self.token.val not in val

            while self.token.typ != typ and valCond():
                if self.token.typ == TT.EOF:
                    break
                self.nxtTok()

    def error(self, errCls: type[err.Err], msg: str, token: tok.Token) -> None:
        """
        Display an error message.
        > param errCls: The error class
        > param msg: The error message
        > param token: The offending token
        """
        if errCls not in self.availErrs:
            raise err.LogicalErr.NoSuchErr(f"No such parser error class: '{errCls.__name__}'")
        errCls(msg, token.pos, token.ln, token.ppos)

    def _getUnexpTokMsg(
        self,
        token: tok.Token,
        exptd: (
            tok.Token
            | TT
            | list[tok.Token]
            | list[TT]
            | tuple[tok.Token, ...]
            | tuple[TT, ...]
            | None
        ),
        exactMatch: bool = False,
    ) -> str:
        """
        Get the error message for an unexpected token.
        > param token: The unexpected token
        > param exptd: The expected token types
        > param exactMatch: Whether to match the tokens/types exactly
        """
        # No expected tokens
        if not exptd:
            return f"Unexpected token '{token.val}' ({token.typ.name})"

        if isinstance(exptd, (list, tuple)):
            res, first = ugen.isUnifTyp(exptd, exactMatch=exactMatch, noEmpty=True)
            if not res:
                raise err.LogicalErr.ArrElemTypErr("Multiple types in array 'exptd'")

            # Get display string for expected types
            if isinstance(first, tok.Token):
                exptdStr = "/".join(f"'{t.val}' ({t.typ.name})" for t in exptd)
            elif isinstance(first, TT):
                exptdStr = "/".join(t.name for t in exptd)
            else:
                raise err.LogicalErr.ArrElemTypErr("Invalid type in array 'exptd'")

            return f"Expected {exptdStr}, got '{token.val}' ({token.typ.name})"

        elif isinstance(exptd, tok.Token):
            return f"Expected '{exptd.val}' ({exptd.typ.name}), got {token.val} ({token.typ.name})"

        elif isinstance(exptd, TT):  # type: ignore
            return f"Expected {exptd.name}, got '{token.val}' ({token.typ.name})"

        elif isinstance(exptd, str):  # type: ignore
            return f"Expected '{exptd}', got '{token.val}' ({token.typ.name})"

        else:
            raise err.LogicalErr.InvTyp(
                "Invalid type for param 'exptd' in parser.Parser._getUnexpTokMsg(...)"
            )

    def _repUnexpTok(
        self,
        token: tok.Token,
        exptd: (
            tok.Token
            | TT
            | list[tok.Token]
            | list[TT]
            | tuple[tok.Token, ...]
            | tuple[TT, ...]
            | None
        ) = None,
        exactMatch: bool = False,
    ) -> None:
        """
        Report an unexpected token.
        > param token: The unexpected token
        > param exptd: The expected token types
        > param exactMatch: Whether to match the tokens/types exactly
        """
        self.error(
            err.ParserErr.unexpTok,
            self._getUnexpTokMsg(token, exptd, exactMatch),
            token,
        )
        self.skipTillResyncToks()

    def _match(
        self,
        typ: TT | list[TT] | tuple[TT, ...],
        val: ty.Any = None,
        goToNxtTok: bool = True,
    ) -> tuple[tok.Token, int]:
        """
        Match a token based on its type, and value if given.
        > param typ: The token type to match
        > param val: The token value to match
        > param goToNxtTok: Whether to advance to the next token
        > return: A tuple of the matched token and an integer error code
        """
        curTok = self.token
        advTok = True
        err = uconst.ERR_SUCCESS

        # Match token type from list/tuple of values
        if isinstance(typ, (list, tuple)):
            if [i for i in typ if i == curTok.typ]:
                self.nxtTok() if goToNxtTok else None
            else:
                self._repUnexpTok(curTok, typ)
                advTok = False
                err = err or self.ERR_MATCH_TOK_ERR

            self.nxtTok() if goToNxtTok and advTok else None
            return curTok, err

        if self.token.typ != typ:
            self._repUnexpTok(self.token, typ)
            advTok = False
            err = err or self.ERR_MATCH_TOK_ERR

        if val is not None and self.token.val != val:
            self._repUnexpTok(self.token, val)
            advTok = False
            err = err or self.ERR_MATCH_TOK_ERR

        self.nxtTok() if goToNxtTok and advTok else None
        return curTok, err

    def parse(self) -> list[ast.ASTNode]:
        """
        Entry point to start parsing.
        > return: A list of AST nodes, i.e. the AST obtained after parsing
        """
        tmp = self.parseCfg()

        # Var tmp being a list indicates a problem
        if isinstance(tmp, list):
            for i in tmp:
                self.parseErrsAdd(i.typStr, i.token)
        else:
            self.treeApp(tmp)

        self.skipWSToks()

        while self.token.typ != TT.EOF:
            tmp = self.parseStmt()
            if isinstance(tmp, ast.ErrNode):
                self.parseErrsAdd(tmp.typStr, tmp.token)
                continue
            self.treeApp(tmp)

        return self.tree
