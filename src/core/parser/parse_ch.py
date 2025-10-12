import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
CH_ESTRS = uetstr.ChETS


class ChParserMixin(pproto.ParserProtocol):
    def parseCh(self) -> ast.ChNode | ast.ErrNode:
        """
        Parse a let statement.
        > return: Statement node of the parsed let statement or an error node
        """
        # Keyword ch
        if not self.chkTok(TT.KEYWD, "ch"):
            return ast.ErrNode(CH_ESTRS.noChKeywd, self.token)
        chTok = self.token
        self.nxtTok()

        # Identifier
        if not self.chkTok(TT.IDENT):
            return ast.ErrNode(CH_ESTRS.noIdent, self.token)
        ident = ast.IdentNode(self.token)
        self.nxtTok()

        # '='
        if not self.chkTok(TT.EQ):
            return ast.ErrNode(CH_ESTRS.noEq, self.token)
        self.nxtTok()

        # Expression
        expr = self.parseExpr()
        if isinstance(expr, ast.ErrNode):
            return ast.ErrNode(CH_ESTRS.exprErr, expr.token)
        return ast.ChNode(ident, expr, chTok)
