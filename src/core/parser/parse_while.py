import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
WHILE_ESTRS = uetstr.WhileETS


class WhileParserMixin(pproto.ParserProtocol):
    def parseWhile(self) -> ast.WhileNode | ast.ErrNode:
        # Keyword while
        if not self.chkTok(TT.KEYWD, "while"):
            return ast.ErrNode(WHILE_ESTRS.noWhile, self.token)
        whileTok = self.token
        self.nxtTok()

        # Condition, i.e. an expression
        cond = self.parseExpr()
        if type(cond) == ast.ErrNode:
            return ast.ErrNode(WHILE_ESTRS.exprErr, self.token, cond)

        # Body of the while statement
        body = self.parseCmpndStmt()
        if type(body) == ast.ErrNode:
            return ast.ErrNode(WHILE_ESTRS.bodyErr, self.token, body)

        # TODO: Add the else construct if needed

        return ast.WhileNode(cond, body, whileTok)
