import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
IF_ESTRS = uetstr.IfETS


class IfParserMixin(pproto.ParserProtocol):
    def parseIf(self) -> ast.IfNode | ast.ErrNode:
        # Keyword if
        if not self.chkTok(TT.KEYWD, "if"):
            return ast.ErrNode(IF_ESTRS.noIf, self.token)
        ifTok = self.token
        self.nxtTok()

        # Condition, i.e. an expression
        cond = self.parseExpr()
        if type(cond) == ast.ErrNode:
            return ast.ErrNode(IF_ESTRS.exprErr, self.token, cond)

        # Body of the if statement
        body = self.parseCmpndStmt()
        if type(body) == ast.ErrNode:
            return ast.ErrNode(IF_ESTRS.bodyErr, self.token, body)

        # TODO: Add elif and else constructs

        return ast.IfNode(cond, body, ifTok)
