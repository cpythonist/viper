import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.sem_err_typ_strs as uetstrs


class LetAnalyserMixin(semproto.SemalyserProtocol):
    def analyseLetNode(self, node: ast.LetNode, scope: str) -> str | None:
        msg, exprTyp, _, _, _ = self.typChkExprs(node.expr, scope)
        if msg != uetstrs.allGood:
            return msg

        if node.typ != exprTyp:
            return uetstrs.LetStmtETS.typMismatch
        else:
            self.symTable.setVar(scope, node.ident.nm, node.typ)
