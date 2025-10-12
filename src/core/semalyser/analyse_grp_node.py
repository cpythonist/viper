import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.sem_err_typ_strs as uetstrs


class GrpAnalyserMixin(semproto.SemalyserProtocol):
    def analyseGrpNode(self, node: ast.GrpNode, scope: str) -> str | None:
        msg, _, _, _, _ = self.typChkExprs(node.node, scope)
        if msg != uetstrs.allGood:
            return msg
