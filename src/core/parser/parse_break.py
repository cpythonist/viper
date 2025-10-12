import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
BREAK_ESTRS = uetstr.BreakETS


class BreakParserMixin(pproto.ParserProtocol):
    def parseBreak(self) -> ast.BreakNode | ast.ErrNode:
        self.skipWSToks()

        if not self.chkTok(TT.KEYWD, "break"):
            return ast.ErrNode(BREAK_ESTRS.noBreak, self.token)
        self.nxtTok()

        return ast.BreakNode(self.token)
