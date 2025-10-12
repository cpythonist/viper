import typing as ty

import core.ast_nodes as ast
import core.token_ as tok

TT = tok.TokenTypes
allNodeTyps = (
    ast.CfgNode
    | ast.LetNode
    | ast.IfNode
    | ast.WhileNode
    | ast.BreakNode
    | ast.ContiNode
    | ast.PrnNode
    | ast.FnNode
    | ast.StmtNode
    | ast.NotImplementedNode
    | ast.ErrNode
)


class ASTPruner:
    def __init__(self, tree: list[ast.ASTNode]) -> None:
        self.constFoldTyps: dict[TT, ty.Callable[..., ty.Any]]
        self.pyToVipBools: dict[bool | str, bool | str]

        self.constFoldTyps = {TT.INT: int, TT.FLOAT: float, TT.BOOL: bool, TT.STR: str}
        self.pyToVipBools = {True: "true", False: "false"}
        self.vipToPyBools = {"true": True, "false": False}
        self.tree = tree

    def prune(self) -> None:
        """
        Prune the AST.
        """
        tmp: list[ast.ASTNode]

        # Remove empty statements from the tree
        self.tree = self._rmEmpStmts(self.tree)

        # TODO: Refactor self._constFolding to handle iteration over the AST by itself
        # Constant folding
        tmp = []
        tmpApp = tmp.append
        for node in self.tree:
            if type(node) == ast.ErrNode:
                tmpApp(node)
                continue
            try:
                tmpApp(self._constFolding(node))
            except OverflowError:
                tmpApp(ast.ErrNode("expr-overflow", node.token, node))
        self.tree = list(tmp)

        # Remove if/while nodes that are empty or whose condition evaluates to false
        tmp = []
        tmpApp = tmp.append
        for node in self.tree:
            if type(node) == ast.ErrNode:
                tmpApp(node)
                continue
            res = self._chkIfEmpOrFalseIfWhileNode(node)
            if isinstance(res, ast.ASTNode):
                tmpApp(res)
            elif res is None:
                # Not needed, but has been put here for the sake of clarity, at least for now
                pass
        self.tree = list(tmp)

    def _rmEmpStmts(self, nodeList: list[ast.ASTNode]) -> list[ast.ASTNode]:
        """
        Remove empty statement nodes from the AST.
        > param nodeList: The list of AST nodes
        > return: A list of AST nodes without empty statement nodes
        """
        for idx in reversed(range(len(nodeList))):
            node = nodeList[idx]
            if type(node) == ast.StmtNode:
                self._rmEmpStmts(node.nodes)
                if not node.nodes:
                    del nodeList[idx]
            elif type(node) == ast.IfNode or type(node) == ast.WhileNode:
                self._rmEmpStmts([node.body])

        return nodeList

    def _chkIfEmpOrFalseIfWhileNode(self, node: ast.ASTNode) -> ast.ASTNode | None:
        """
        Check if an if/while node is empty, or its condition evaluates to false.
        > param node: AST node to be evaluated
        > return: ASTNode if the node is not an if/while node or its condition evaluates to true.
                  None otherwise.
        """
        # Not a IfNode/WhileNode obj
        if type(node) != ast.IfNode and type(node) != ast.WhileNode:
            return node

        # Non-literal condition
        if type(node.cond) != ast.LiteralNode:  # type: ignore
            return node

        # No body, i.e. no stmts
        if not node.body.nodes:
            return None

        isIntAndZero = node.cond.token.typ == TT.INT and node.cond.token.val == "0"
        isFloatAndZero = node.cond.token.typ == TT.FLOAT and node.cond.token.val == "0.0"
        isBoolAndFalse = node.cond.token.typ == TT.BOOL and node.cond.token.val == "false"
        isStrAndEmp = node.cond.token.typ == TT.STR and node.cond.token.val == ""

        # Cond evals to true or not a basic type
        if not (isIntAndZero or isFloatAndZero or isBoolAndFalse or isStrAndEmp):
            return node

        return None

    def _helperUnaryConstFolding(self, node: ast.UnaryOpNode) -> ast.ASTNode:
        node.rt = self._constFolding(node.rt)  # type: ignore

        if type(node.rt) != ast.LiteralNode:
            return node

        if node.rt.token.typ not in (TT.INT, TT.FLOAT):
            return node

        opPos = node.op.pos
        opLn = node.op.ln
        opPpos = node.op.ppos
        opTyp = node.op.typ
        fn = self.constFoldTyps[node.rt.typ]
        rtVal = fn(node.rt.token.val)
        if opTyp == TT.PLUS:
            rtVal = +rtVal
        elif opTyp == TT.MINUS:
            rtVal = -rtVal

        return ast.LiteralNode(tok.Token(node.rt.typ, str(rtVal), opPos, opLn, opPpos))

    def _constFolding(self, node: ast.ASTNode) -> ast.ASTNode:
        # TODO: Refactor this long ass method to include smaller helper methods.
        # NOTE: isinstance(...) calls haven't been used so as to not eval to True is the type is a
        # child class
        if type(node) == ast.StmtNode:
            node.nodes = [tmp for n in node.nodes if (tmp := self._constFolding(n)) is not None]  # type: ignore

        elif type(node) == ast.PrnNode:
            node.expr = self._constFolding(node.expr)  # type: ignore

        elif type(node) == ast.GrpNode:
            node.node = self._constFolding(node.node)  # type: ignore
            if type(node.node) == ast.LiteralNode:
                node = node.node  # type: ignore

        elif type(node) == ast.UnaryOpNode:
            self._helperUnaryConstFolding(node)

        elif type(node) == ast.BinOpNode:
            # What the hell is this convuluted mess?
            node.lt = self._constFolding(node.lt)  # type: ignore
            node.rt = self._constFolding(node.rt)  # type: ignore

            # /* This condition was expanded from type(node.lt) == type(node.rt) == ast.LiteralNode
            # to shut the linter up. */
            if type(node.lt) == ast.LiteralNode and type(node.rt) == ast.LiteralNode:
                ltPos = node.lt.token.pos
                ltLn = node.lt.token.ln
                ltPPos = node.lt.token.ppos
                fn = self.constFoldTyps[node.lt.typ]

                if node.lt.typ == TT.IDENT or node.rt.typ == TT.IDENT:
                    return node

                opTyp = node.op.typ
                ltTyp = node.lt.typ
                ltVal = node.lt.val
                rtTyp = node.rt.typ
                rtVal = node.rt.val
                res = None

                if ltTyp != rtTyp:
                    return node

                fn = self.constFoldTyps[ltTyp]
                ltValConvd = fn(ltVal) if ltTyp != TT.BOOL else self.vipToPyBools[ltVal]
                rtValConvd = fn(rtVal) if rtTyp != TT.BOOL else self.vipToPyBools[rtVal]

                if opTyp == TT.PLUS:
                    if ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd + rtValConvd

                elif opTyp == TT.MINUS:
                    if ltTyp == TT.STR:
                        res = ltVal.replace(rtVal, "")
                    elif ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd - rtValConvd

                elif opTyp == TT.ASTERISK:
                    if ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd * rtValConvd

                elif opTyp == TT.FSLASH:
                    if not rtValConvd:
                        node = ast.ErrNode("expr-zero-div", node.token, node)
                        res = None
                    elif ltTyp == TT.INT:
                        res = int(ltValConvd / rtValConvd)
                    elif ltTyp == TT.FLOAT:
                        res = ltValConvd / rtValConvd

                elif opTyp == TT.DOLLAR:
                    if not rtValConvd:
                        node = ast.ErrNode("expr-zero-div", node.token, node)
                        res = None
                    elif ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd // rtValConvd

                elif opTyp == TT.PERCENT:
                    if not rtValConvd:
                        node = ast.ErrNode("expr-zero-div", node.token, node)
                        res = None
                    elif ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd % rtValConvd

                elif opTyp == TT.CARET:
                    if ltTyp in (TT.INT, TT.FLOAT):
                        res = ltValConvd**rtValConvd

                elif opTyp == TT.EQEQ:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.BOOL, TT.STR):
                        res = ltValConvd == rtValConvd

                elif opTyp == TT.NEQ:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.BOOL, TT.STR):
                        res = ltValConvd != rtValConvd

                elif opTyp == TT.LT:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.STR):
                        res = ltValConvd < rtValConvd

                elif opTyp == TT.LTEQ:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.STR):
                        res = ltValConvd <= rtValConvd

                elif opTyp == TT.GT:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.STR):
                        res = ltValConvd > rtValConvd

                elif opTyp == TT.GTEQ:
                    if ltTyp in (TT.INT, TT.FLOAT, TT.STR):
                        res = ltValConvd >= rtValConvd

                if res is not None:
                    if isinstance(res, bool):
                        ltTyp = TT.BOOL
                        res = self.pyToVipBools[res]
                    node = ast.LiteralNode(tok.Token(ltTyp, str(res), ltPos, ltLn, ltPPos))

        elif type(node) == ast.IfNode or type(node) == ast.WhileNode:
            node.cond = self._constFolding(node.cond)  # type: ignore
            node.body = self._constFolding(node.body)  # type: ignore

        elif type(node) == ast.LetNode:
            node.expr = self._constFolding(node.expr)  # type: ignore

        return node
