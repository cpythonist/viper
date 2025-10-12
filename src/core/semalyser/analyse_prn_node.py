import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.sem_err_typ_strs as uetstrs


class PrnAnalyserMixin(semproto.SemalyserProtocol):
    def analysePrnNode(self, node: ast.PrnNode, scope: str) -> str | None:
        msg, _, _, _, _ = self.typChkExprs(node.expr, scope)
        if msg != uetstrs.allGood:
            return msg
