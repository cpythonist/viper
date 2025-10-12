import core.ast_nodes as ast

import core.ir_gen.protocol as irproto


class LetIRGenMixin(irproto.IRGenProtocol):
    def genLetIR(self, node: ast.LetNode) -> tuple[str, str, str, str]:
        exprIR = self.genExprIR(node.expr)
        # TODO: Eppidi itha vadivamaikkalamnu yoesi
        # return ('=', node.ident.nm, exprIR, node.typ)
