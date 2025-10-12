import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
PRN_ESTRS = uetstr.PrnETS


class PrnParserMixin(pproto.ParserProtocol):
    def parsePrn(self) -> ast.PrnNode | ast.ErrNode:
        # Keyword prn
        if not self.chkTok(TT.KEYWD, "prn"):
            return ast.ErrNode(PRN_ESTRS.noPrnKeywd, self.token)
        prnTok = self.token
        self.nxtTok()

        # Expression
        expr = self.parseExpr()
        if type(expr) == ast.ErrNode:
            return ast.ErrNode(PRN_ESTRS.exprErr, self.token, expr)

        return ast.PrnNode(expr, prnTok)
