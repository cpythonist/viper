import sys

import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.gen as ugen
import utils.sem_err_typ_strs as uetstrs


class ChAnalyserMixin(semproto.SemalyserProtocol):
    def analyseChNode(self, node: ast.ChNode, scope: str) -> str | None:
        currScope = self.symTable.get(scope)
        if currScope is None:
            ugen.fatal(f"Scope not found for ChNode: '{scope}'", None)
            sys.exit(-1)

        if node.ident.nm not in currScope:
            return uetstrs.ChStmtETS.noSuchVar

        msg, exprTyp, _, _, _ = self.typChkExprs(node.expr, scope)
        if msg != uetstrs.allGood:
            return msg

        if currScope[node.ident.nm] != exprTyp:
            return uetstrs.ChStmtETS.typMismatch
