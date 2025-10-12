import core.semalyser.protocol as semproto

import core.ast_nodes as ast

import utils.sem_err_typ_strs as uetstrs


class RetAnalyserMixin(semproto.SemalyserProtocol):
    def analyseRetNode(
        self, node: ast.RetNode, scope: str, parentNode: ast.ASTNode | None
    ) -> str | None:
        corresFnNode = parentNode

        while corresFnNode is not None and type(corresFnNode) != ast.FnNode:
            corresFnNode = corresFnNode.parent

        if type(corresFnNode) != ast.FnNode:
            return uetstrs.RetStmtETS.notInsideFn

        msg, exprTyp, _, _, _ = self.typChkExprs(node.expr, scope)
        if msg != uetstrs.allGood:
            return msg

        if corresFnNode.typ != exprTyp:
            return uetstrs.RetStmtETS.typMismatch
