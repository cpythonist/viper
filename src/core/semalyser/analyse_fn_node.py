import copy

import core.semalyser.protocol as semproto

import core.ast_nodes as ast


class FnAnalyserMixin(semproto.SemalyserProtocol):
    def analyseFnNode(self, node: ast.FnNode, scope: str) -> None:
        fnScopeNm = f"fn{self.nodeNo}"
        self.symTable.crtScope(fnScopeNm, copy.deepcopy(node.params), scope, isFn=True)
        self.analyseTree(node.body.nodes, fnScopeNm, node)
        self.symTable.rmScope(fnScopeNm)
