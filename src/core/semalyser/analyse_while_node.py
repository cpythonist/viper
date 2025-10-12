import copy

import core.ast_nodes as ast

import core.semalyser.protocol as semproto

import utils.gen as ugen
import utils.sem_err_typ_strs as uetstrs


class WhileAnalyserMixin(semproto.SemalyserProtocol):
    def analyseWhileNode(self, node: ast.WhileNode, scope: str) -> str | None:
        whileScopeNm = f"while{self.nodeNo}"

        msg, _, _, _, _ = self.typChkExprs(node.cond, scope)
        if msg != uetstrs.allGood:
            return msg

        currScope = self.symTable.get(scope)
        if currScope is None:
            ugen.fatal(f"Current scope not found for {whileScopeNm}: '{scope}'", -1)

        # Create a separate scope for the while-loop
        self.symTable.crtScope(
            scopeNm=whileScopeNm,
            initVals=copy.deepcopy(currScope.allVars),
            parent=currScope.nm,
            isFn=False,
        )
        self.analyseTree(node.body.nodes, whileScopeNm, node)
        self.symTable.rmScope(whileScopeNm)
