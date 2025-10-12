import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
CONTI_ESTRS = uetstr.ContiETS


class ContiParserMixin(pproto.ParserProtocol):
    def parseConti(self) -> ast.ContiNode | ast.ErrNode:
        self.skipWSToks()

        if not self.chkTok(TT.KEYWD, "conti"):
            return ast.ErrNode(CONTI_ESTRS.noConti, self.token)
        self.nxtTok()

        return ast.ContiNode(self.token)
