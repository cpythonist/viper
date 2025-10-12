import core.semalyser.protocol as semproto

import core.ast_nodes as ast


class StmtAnalyserMixin(semproto.SemalyserProtocol):
    def analyseStmtNode(self, node: ast.StmtNode, scope: str) -> ast.StmtNode | str:
        """
        Analyse a statement node by analysing each of its child nodes.
        > param node: The statement node to analyse.
        > param scope: The current scope name.
        """
        stmtNodeList: list[ast.ASTNode]
        stmtNodeList = []
        stmtNodeListApp = stmtNodeList.append

        for n in node.nodes:
            tmp, nodeProb = self.analyseNode(n, scope, node)
            if not nodeProb:
                stmtNodeListApp(tmp)

        node.nodes = stmtNodeList
        node.parent = node
        return node
