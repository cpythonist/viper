import core.ast_nodes as ast
import core.token_ as tok
import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstrs

TT = tok.TokenTypes
RET_ESTRS = uetstrs.RetETS


class RetParserMixin(pproto.ParserProtocol):
    def parseRet(self) -> ast.RetNode | ast.ErrNode:
        self.skipWSToks()

        if not self.chkTok(TT.KEYWD, "ret"):
            return ast.ErrNode(RET_ESTRS.noRetKeywd, self.token)
        retTok = self.token
        self.nxtTok()

        expr = self.parseExpr()
        if type(expr) == ast.ErrNode:
            return ast.ErrNode(RET_ESTRS.exprErr, expr.token)

        return ast.RetNode(expr, retTok)
