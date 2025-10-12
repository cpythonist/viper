import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
LET_ESTRS = uetstr.LetETS


class LetParserMixin(pproto.ParserProtocol):
    def parseLet(self) -> ast.LetNode | ast.ErrNode:
        """
        Parse a let statement.
        > return: Statement node of the parsed let statement or an error node
        """
        varTyp: TT

        # Keyword let
        if not self.chkTok(TT.KEYWD, "let"):
            return ast.ErrNode(LET_ESTRS.noLetKeywd, self.token)
        letTok = self.token
        self.nxtTok()

        # Type keyword
        if not (
            self.chkTok(TT.KEYWD) and self.chkTokRange((1000, 1099), TT[self.token.val.upper()])
        ):  # type: ignore
            return ast.ErrNode(LET_ESTRS.noTypKeywd, self.token)
        varTyp = TT[self.token.val.upper()]  # type: ignore
        self.nxtTok()

        # Identifier
        if not self.chkTok(TT.IDENT):
            return ast.ErrNode(LET_ESTRS.noIdent, self.token)
        ident = ast.IdentNode(self.token)
        self.nxtTok()

        # '='
        if not self.chkTok(TT.EQ):
            return ast.ErrNode(LET_ESTRS.noEq, self.token)
        self.nxtTok()

        # Expression
        expr = self.parseExpr()
        if isinstance(expr, ast.ErrNode):
            return ast.ErrNode(LET_ESTRS.exprErr, expr.token)

        return ast.LetNode(ident, varTyp, expr, letTok)
