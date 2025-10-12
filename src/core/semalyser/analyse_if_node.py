import copy

import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.gen as ugen
import utils.sem_err_typ_strs as uetstrs


class IfAnalyserMixin(semproto.SemalyserProtocol):
    def analyseIfNode(self, node: ast.IfNode, scope: str) -> str | None:
        ifScopeNm = f"if{self.nodeNo}"

        msg, _, _, _, _ = self.typChkExprs(node.cond, scope)
        if msg != uetstrs.allGood:
            return msg

        currScope = self.symTable.get(scope)
        if currScope is None:
            ugen.fatal(f"Current scope not found for {ifScopeNm}: '{scope}'", -1)

        # Create a separate scope for the if-statement
        self.symTable.crtScope(
            scopeNm=ifScopeNm,
            initVals=copy.deepcopy(currScope.allVars),
            parent=currScope.nm,
            isFn=False,
        )
        self.analyseTree(node.body.nodes, ifScopeNm, node)
        self.symTable.rmScope(ifScopeNm)
